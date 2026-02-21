from models.database import Database
from typing import Optional, Self, Any
from sqlite3 import Cursor
from datetime import datetime

class Tarefa:
    def __init__(self: Self, 
                 titulo_tarefa: Optional[str] = None, 
                 data_conclusao: Optional[str] = None, 
                 id_tarefa: Optional[int] = None, 
                 concluida: Optional[int] = 0,
                 data_conclusao_real: Optional[str] = None) -> None:
        self.titulo_tarefa: Optional[str] = titulo_tarefa
        self.data_conclusao: Optional[str] = data_conclusao
        self.id_tarefa: Optional[int] = id_tarefa
        self.concluida: Optional[int] = concluida
        self.data_conclusao_real: Optional[str] = data_conclusao_real

    @classmethod
    def id(cls, id_tarefa: int) -> Self:
        with Database() as db:
            query: str = 'SELECT titulo_tarefa, data_conclusao, concluida, data_conclusao_real FROM tarefas WHERE id = ?;'
            params: tuple = (id_tarefa,)
            resultado: tuple = db.buscar_um(query, params)
            if not resultado:
                raise ValueError(f"Tarefa com ID {id_tarefa} não encontrada")
            titulo, data_conclusao, concluida, data_real = resultado
        return cls(titulo_tarefa=titulo, data_conclusao=data_conclusao, id_tarefa=id_tarefa, concluida=concluida, data_conclusao_real=data_real)

    def salvar_tarefa(self: Self) -> None:
        with Database() as db:
            query: str = "INSERT INTO tarefas (titulo_tarefa, data_conclusao, concluida) VALUES (?,?,?);"
            params: tuple = (self.titulo_tarefa, self.data_conclusao, self.concluida)
            db.executar(query, params)
            self.id_tarefa = db.cursor.lastrowid

    @classmethod
    def obter_tarefas(cls) -> list[Self]:
        with Database() as db:
            query: str = 'SELECT id, titulo_tarefa, data_conclusao, concluida, data_conclusao_real FROM tarefas;'
            resultados: list[tuple] = db.buscar_tudo(query)
            tarefas: list[Self] = [cls(titulo, data, id_, concluida, data_real) 
                                  for id_, titulo, data, concluida, data_real in resultados]
            return tarefas
        
    def excluir_tarefa(self) -> Cursor:
        if self.concluida == 1:
            raise ValueError("Tarefa concluída não pode ser excluída sem reabrir primeiro.")
        with Database() as db:
            query: str = 'DELETE FROM tarefas WHERE id = ?;'
            params: tuple = (self.id_tarefa,)
            resultado: Cursor = db.executar(query, params)
        return resultado
        
    def toggle_concluir(self) -> Cursor:
        with Database() as db:
            if self.concluida == 1:
                query = "UPDATE tarefas SET concluida = 0, data_conclusao_real = NULL WHERE id = ?;"
                params = (self.id_tarefa,)
            else:
                agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                query = "UPDATE tarefas SET concluida = 1, data_conclusao_real = ? WHERE id = ?;"
                params = (agora, self.id_tarefa)
            resultado = db.executar(query, params)
        return resultado
        
    def atualizar_tarefa(self) -> Cursor:
        with Database() as db:
            query: str = 'UPDATE tarefas SET titulo_tarefa = ?, data_conclusao = ?, concluida = 0 WHERE id = ?;'
            params: tuple = (self.titulo_tarefa, self.data_conclusao, self.id_tarefa)
            resultado: Cursor = db.executar(query, params)
        return resultado