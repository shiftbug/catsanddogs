import sqlite3
from typing import List, Optional
from datetime import datetime
from models import ObservableFeatures, AnimalSaleEntry

def get_all_clients(conn: sqlite3.Connection) -> List[str]:
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT client_name FROM animal_sales ORDER BY client_name")
    return [row[0] for row in cursor.fetchall()]

def search_sales(conn: sqlite3.Connection, features: ObservableFeatures, client: Optional[str] = None) -> List[AnimalSaleEntry]:
    cursor = conn.cursor()
    
    # First, try to match by breed
    query = """
    SELECT * FROM animal_sales
    WHERE species LIKE ?
    AND breed LIKE ?
    """
    params = [f"%{features.species}%", f"%{features.breed}%"]

    if client and client != "Any":
        query += " AND client_name = ?"
        params.append(client)

    query += " ORDER BY date DESC LIMIT 5"
    
    print(f"Executing breed match query: {query}")
    print(f"With parameters: {params}")

    cursor.execute(query, params)
    results = cursor.fetchall()

    # If no results, try matching by coat color and/or length
    if not results:
        query = """
        SELECT * FROM animal_sales
        WHERE species LIKE ?
        AND (coat_color LIKE ? OR coat_length LIKE ?)
        """
        params = [
            f"%{features.species}%",
            f"%{features.coat_color}%" if features.coat_color else "%",
            f"%{features.coat_length}%" if features.coat_length else "%"
        ]

        if client and client != "Any":
            query += " AND client_name = ?"
            params.append(client)

        query += " ORDER BY date DESC LIMIT 5"
        
        print(f"Executing coat match query: {query}")
        print(f"With parameters: {params}")

        cursor.execute(query, params)
        results = cursor.fetchall()

    print(f"Number of results: {len(results)}")

    return [AnimalSaleEntry(
        id=row[0],
        date=datetime.strptime(row[1], "%Y-%m-%d"),
        species=row[2],
        breed=row[3],
        size=row[4],
        weight=row[5],
        coat_length=row[6],
        coat_color=row[7],
        price=row[8],
        client_name=row[9],
        client_email=row[10]
    ) for row in results]