import requests
from pulp import LpMaximize, LpProblem, LpVariable, lpSum
import logging
import sqlite3
from typing import List, Dict, Any
from contextlib import contextmanager
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self, db_path: str = "morpho_markets.db"):
        """
        Initialize the database manager.
        
        Args:
            db_path (str): Path to SQLite database file
        """
        self.db_path = db_path
        self.init_database()

    @contextmanager
    def get_connection(self):
        """Context manager for database connections."""
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
        finally:
            conn.close()

    def init_database(self):
        """Initialize database tables if they don't exist."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Create markets table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS markets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    unique_key TEXT NOT NULL,
                    token_symbol TEXT NOT NULL,
                    token_address TEXT NOT NULL,
                    supply_apy REAL,
                    borrow_apy REAL,
                    utilization REAL,
                    lltv REAL,
                    max_supply REAL,
                    risk REAL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create allocations table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS allocations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    market_key TEXT NOT NULL,
                    allocated_amount REAL,
                    available_funds REAL,
                    max_risk REAL,
                    max_utilization REAL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.commit()

    def store_market_data(self, market_data: List[Dict[str, Any]]):
        """
        Store market data in the database.
        
        Args:
            market_data (List[Dict[str, Any]]): List of market data to store
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            for market in market_data:
                cursor.execute("""
                    INSERT INTO markets (
                        unique_key, token_symbol, token_address, 
                        supply_apy, borrow_apy, utilization, 
                        lltv, max_supply, risk
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    market['market'],
                    market['token']['symbol'],
                    market['token']['address'],
                    market['supply_apy'],
                    market['borrow_apy'],
                    market['utilization'],
                    market['lltv'],
                    market['max_supply'],
                    market['risk']
                ))
            
            conn.commit()

    def store_allocation_results(self, allocations: Dict[str, float], params: Dict[str, float]):
        """
        Store allocation results in the database.
        
        Args:
            allocations (Dict[str, float]): Allocation results by market
            params (Dict[str, float]): Optimization parameters
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            for market_key, amount in allocations.items():
                cursor.execute("""
                    INSERT INTO allocations (
                        market_key, allocated_amount, available_funds,
                        max_risk, max_utilization
                    ) VALUES (?, ?, ?, ?, ?)
                """, (
                    market_key,
                    amount,
                    params['available_funds'],
                    params['max_risk'],
                    params['max_utilization']
                ))
            
            conn.commit()

    def get_historical_market_data(self, market_key: str, days: int = 30) -> List[Dict]:
        """
        Retrieve historical market data for analysis.
        
        Args:
            market_key (str): Market identifier
            days (int): Number of days of historical data to retrieve
            
        Returns:
            List[Dict]: Historical market data
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM markets 
                WHERE unique_key = ? 
                AND timestamp >= datetime('now', ?) 
                ORDER BY timestamp DESC
            """, (market_key, f'-{days} days'))
            
            columns = [description[0] for description in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

class MorphoMarketOptimizer:
    def __init__(self, api_url: str = "https://blue-api.morpho.org/graphql"):
        """
        Initialize the Morpho Market Optimizer.
        
        Args:
            api_url (str): Morpho API URL
        """
        self.api_url = api_url
        self.db = DatabaseManager()

    def fetch_market_data(self) -> List[Dict[str, Any]]:
        """
        Fetch market data from Morpho API and store in database.
        
        Returns:
            List[Dict[str, Any]]: List of market data
        """
        query = """
        query {
            markets {
                items {
                    uniqueKey
                    lltv
                    oracleAddress
                    irmAddress
                    loanAsset {
                        address
                        symbol
                        decimals
                    }
                    collateralAsset {
                        address
                        symbol
                        decimals
                    }
                    state {
                        borrowApy
                        borrowAssets
                        borrowAssetsUsd
                        supplyApy
                        supplyAssets
                        supplyAssetsUsd
                        fee
                        utilization
                    }
                }
            }
        }
        """
        
        try:
            response = requests.post(self.api_url, json={"query": query})
            response.raise_for_status()
            data = response.json()
            
            parsed_data = self._parse_market_data(data)
            self.db.store_market_data(parsed_data)

            return parsed_data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch market data: {str(e)}")
            raise

    def _parse_market_data(self, data: Dict) -> List[Dict[str, Any]]:
        """Parse the raw market data into a structured format."""
        parsed_markets = []
        
        for market in data["data"]["markets"]["items"]:
            market_info = {
                "market": market["uniqueKey"],
                "token": market["loanAsset"],
                "borrow_apy": float(market["state"]["borrowApy"] or 0.0),
                "supply_apy": float(market["state"]["supplyApy"] or 0.0),
                "utilization": float(market["state"]["utilization"] or 0.0),
                "lltv": float(market["lltv"] or 0.0),
                "max_supply": float(market["state"]["supplyAssetsUsd"] or 0.0),
                "risk": float(market["state"]["fee"] or 0.0)
            }
            parsed_markets.append(market_info)
            
        return parsed_markets

    def optimize_allocation(self, 
                          available_funds: float, 
                          max_risk: float = 0.2, 
                          max_utilization: float = 0.85) -> Dict[str, float]:
        """Optimize fund allocation across markets using linear programming."""
        market_data = self.fetch_market_data()
        
        # Create optimization problem
        prob = LpProblem("Morpho_Market_Allocation", LpMaximize)
        
        # Define variables
        allocations = {
            market['market']: LpVariable(f"alloc_{market['market']}", 
                                       lowBound=0, 
                                       upBound=market['max_supply'])
            for market in market_data
        }
        
        # Objective: Maximize total APY
        prob += lpSum([
            market['supply_apy'] * allocations[market['market']] 
            for market in market_data
        ])
        
        # Constraints
        prob += lpSum(allocations.values()) <= available_funds
        prob += lpSum([market['risk'] * allocations[market['market']] 
                      for market in market_data]) <= max_risk * available_funds
        prob += lpSum([market['utilization'] * allocations[market['market']] 
                      for market in market_data]) <= max_utilization * available_funds
        
        # Solve and get results
        prob.solve()
        optimized_allocations = {
            market['market']: allocations[market['market']].varValue 
            for market in market_data
        }
        
        # Store results in database
        self.db.store_allocation_results(
            optimized_allocations,
            {
                'available_funds': available_funds,
                'max_risk': max_risk,
                'max_utilization': max_utilization
            }
        )
        
        return optimized_allocations

    def analyze_market_trends(self, market_key: str, days: int = 30) -> Dict[str, Any]:
        """
        Analyze historical trends for a specific market.
        
        Args:
            market_key (str): Market identifier
            days (int): Number of days to analyze
            
        Returns:
            Dict[str, Any]: Analysis results
        """
        historical_data = self.db.get_historical_market_data(market_key, days)
        
        if not historical_data:
            return {"error": "No historical data available"}
        
        # Calculate basic statistics
        supply_apys = [d['supply_apy'] for d in historical_data]
        utilizations = [d['utilization'] for d in historical_data]
        
        analysis = {
            "market_key": market_key,
            "avg_supply_apy": sum(supply_apys) / len(supply_apys),
            "max_supply_apy": max(supply_apys),
            "min_supply_apy": min(supply_apys),
            "avg_utilization": sum(utilizations) / len(utilizations),
            "data_points": len(historical_data),
            "date_range": {
                "start": historical_data[-1]['timestamp'],
                "end": historical_data[0]['timestamp']
            }
        }
        
        return analysis

def main():
    # Initialize optimizer
    optimizer = MorphoMarketOptimizer()
    
    try:
        # Fetch and store current market data
        market_data = optimizer.fetch_market_data()
        logger.info(f"Successfully fetched data for {len(market_data)} markets")
        
        # Optimize allocation
        allocations = optimizer.optimize_allocation(
            available_funds=1_000_000,  # $1M USD
            max_risk=0.2,
            max_utilization=0.85
        )
        
        # Print allocation results
        print("\nOptimized Allocations:")
        for market, amount in allocations.items():
            print(f"{market}: ${amount:,.2f}")
            
        # Analyze trends for a specific market
        # sample_market = list(allocations.keys())[0]
        # trends = optimizer.analyze_market_trends(sample_market)
        # print(f"\nMarket Analysis for {sample_market}:")
        # print(json.dumps(trends, indent=2))
        
    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}")
        raise

if __name__ == "__main__":
    main()