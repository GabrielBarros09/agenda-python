from sqlite3 import Connection, connect, Cursor
from types import TracebackType
from typing import Any, Optional, Self, Type
from dotenv import load_dotenv
import traceback
import os

load_dotenv()

DB_PATH = os.getenv('DATABASE', './data/tarefas.sqlite3')


class Database:
    def __init__(self, db_name: str = DB_PATH) -> None:
        self.connection: Connection = connect(db_name)
        self.cursor: Cursor = self.connection.cursor()

    def executar(self, query: str, params: tuple = ()) -> Cursor:
        self.cursor.execute(query, params)
        self.connection.commit()
        return self.cursor
    
    def buscar_um(self, query: str, params: tuple = ()) -> Any:
        self.cursor.execute(query, params)
        return self.cursor.fetchone()
    
    def buscar_tudo(self, query: str, params: tuple = ()) -> list[Any]:
        self.cursor.execute(query, params)
        return self.cursor.fetchall()
    
    def close(self) -> None:
        self.connection.close()

    def __enter__(self) -> Self:
        return self
    
    def __exit__(self,
                 exc_type: Optional[Type[BaseException]], 
                 exc_value: Optional[BaseException], 
                 tb: Optional[TracebackType]) -> None:
        if exc_type is not None:
            print("Exceção capturada no contexto:")
            print(f'tipo: {exc_type.__name__}')
            print(f'Mensagem: {exc_value}')
            print('Traceback Completo: ')
            traceback.print_tb(tb)

        self.close()