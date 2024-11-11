from typing import Optional

from metasdk.schemas import IssueCreateItem, IssueGetItem
from metasdk.exceptions import BadParametersError

from metasdk.tools.validators import check_postgres_date

class IssueService:

    def __init__(self, app):
        """
        :type app: metasdk.MetaApp
        """
        self.__app = app
        self.__options = {}
        self.__data_get_cache = {}
        self.__metadb = app.db("meta")

    def change_issue_status(self, issue_id, status_id: str):
        """
        Смета статуса тикета
        :param issue_id: int
        :param status_id: int
        """
        self.__metadb.update("""
              update meta.issue set 
                issue_status_id=:status_id,
                assignee_user_id=valera_user_id(),
                last_user_id=valera_user_id()
              where id = :issue_id
        """, {"issue_id": issue_id, "status_id": status_id})

    def pending_issue(self, issue_id):
        """
        Перевести в статус "В ожидании"
        :param issue_id: int
        """
        self.change_issue_status(issue_id, '1')

    def in_progress_issue(self, issue_id):
        """
        Взять в работу
        :param issue_id: int
        """
        self.change_issue_status(issue_id, '2')

    def reject_issue(self, issue_id):
        """
        Отклонить задачу
        :param issue_id: int
        """
        self.change_issue_status(issue_id, '7')

    def clarification_issue(self, issue_id):
        """
        Уточнение
        :param issue_id: int
        """
        self.change_issue_status(issue_id, '4')

    def done_issue(self, issue_id):
        """
        Успешное выполенение
        :param issue_id: int
        """
        self.change_issue_status(issue_id, '3')

    def add_issue_msg(self, issue_id, msg):
        self.__metadb.update("""
            INSERT INTO meta.issue_msg (msg, issue_id, user_id, last_user_id)
            VALUES (:msg, :issue_id, valera_user_id(), valera_user_id())
        """, {"issue_id": issue_id, "msg": msg})

    def create_issue(self, issue: IssueCreateItem) -> int:
        """
        Создание тикета
        :param issue: IssueCreateItem объект с данными тикета
        :return: ticket_id int айди созданного тикета
        """
        query = """
            INSERT INTO meta.issue (
                application_id,
                name,
                description,
                form_data,
                issue_type_id,
                issue_priority_id,
                reporter_user_id,
                last_user_id,
                entity_id,
                object_id,
                deadline_time,
                estimated_time,
                tags,
                watcher_users,
                result,
                assignee_user_id)
            SELECT 
                :application_id::text,
                :issue_name::text,
                :description::text,
                :form_data::jsonb,
                :issue_type_id::text,
                :issue_priority_id::text,
                :reporter_user_id::bigint,
                :last_user_id::bigint,
                :entity_id::text,
                :object_id::text,
                :deadline_time::timestamp,
                :estimated_time::interval,
                :tags::text[],
                :watcher_users::jsonb,
                :result::jsonb,
                :assignee_user_id::bigint
            RETURNING id
        """
        ticket_id = self.__metadb.query(query, {
            "application_id": issue.application_id,
            "issue_name": issue.name,
            "description": issue.description,
            "form_data": issue.form_data,
            "issue_type_id": issue.issue_type_id,
            "issue_priority_id": issue.issue_priority_id,
            "reporter_user_id": issue.reporter_user_id,
            "last_user_id": issue.last_user_id,
            "entity_id": issue.entity_id,
            "object_id": issue.object_id,
            "deadline_time": issue.deadline_time_datetime,
            "estimated_time": issue.estimated_time_interval,
            "tags": issue.tags,
            "watcher_users": issue.watcher_users,
            "result": issue.result,
            "assignee_user_id": issue.assignee_user_id
        })
        return ticket_id.get("rows", [])[0].get("id")

    def get_issue(self, issue_id: int) -> IssueGetItem:
        """
        Возвращает тикет по айди
        :param issue_id: int
        :return: IssueGetItem
        """
        try:
            issue_id = int(issue_id)
        except ValueError:
            raise BadParametersError("Issue id should be integer")
        query = """
            SELECT 
                id,
                name,
                description,
                form_data,
                creation_time,
                modification_time,
                last_user_id,
                issue_type_id,
                reporter_user_id,
                assignee_user_id,
                issue_priority_id,
                issue_status_id,
                entity_id,
                object_id,
                application_id,
                watcher_users,
                deadline_time,
                status_change_time,
                ref_key,
                estimated_time,
                tags,
                result
            FROM meta.issue WHERE id = :id
        """
        issue = self.__metadb.one(query, {"id": issue_id})
        return IssueGetItem(**issue)

    def get_issues(
        self,
        creation_time: Optional[str] = None,
        modification_time: Optional[str] = None,
        issue_type_id: Optional[str] = None,
        issue_status_id: Optional[str] = None,
        assignee_user_id: Optional[int] = None,
        reporter_user_id: Optional[int] = None,
        watcher_users: Optional[list[int]] = None,
    ) -> list[IssueGetItem]:
        """
        Возвращает список тикетов. Выдача ограничена 1000 записями
        :param creation_time: str согласно выдаче метода DbQueryService.all соответсвует формату '%Y-%m-%dT%H:%M:%S.%f%z',
        но может использоваться формат '%Y-%m-%d', так как в запросе приводится к date
        :param modification_time: str согласно выдаче метода DbQueryService.all соответсвует формату '%Y-%m-%dT%H:%M:%S.%f%z',
        но может использоваться формат '%Y-%m-%d', так как в запросе приводится к date
        :param issue_type_id: str
        :param issue_status_id: str
        :param assignee_user_id: int
        :param reporter_user_id: int
        :param watcher_users: list[int]
        :return: list[IssueGetItem]
        """
        if creation_time is not None:
            check_postgres_date(creation_time)
        if modification_time is not None:
            check_postgres_date(modification_time)
        query = """
            SELECT 
                id,
                name,
                description,
                form_data,
                creation_time,
                modification_time,
                last_user_id,
                issue_type_id,
                reporter_user_id,
                assignee_user_id,
                issue_priority_id,
                issue_status_id,
                entity_id,
                object_id,
                application_id,
                watcher_users,
                deadline_time,
                status_change_time,
                ref_key,
                estimated_time,
                tags,
                result
            FROM meta.issue
            WHERE 2>1
                AND CASE WHEN :creation_time::date IS NOT NULL THEN creation_time::date = :creation_time::date ELSE TRUE END
                AND CASE WHEN :modification_time::date IS NOT NULL THEN modification_time::date = :modification_time::date ELSE TRUE END
                AND CASE WHEN :issue_type_id::text IS NOT NULL THEN issue_type_id = :issue_type_id::text ELSE TRUE END
                AND CASE WHEN :issue_status_id::text IS NOT NULL THEN issue_status_id = :issue_status_id::text ELSE TRUE END
                AND CASE WHEN :assignee_user_id::bigint IS NOT NULL THEN assignee_user_id = :assignee_user_id::bigint ELSE TRUE END
                AND CASE WHEN :reporter_user_id::bigint IS NOT NULL THEN reporter_user_id = :reporter_user_id::bigint ELSE TRUE END
                AND CASE WHEN :watcher_users::text IS NOT NULL THEN ARRAY[:watcher_users]::bigint[] <@ ARRAY(
                    SELECT w::bigint as watchers_users_info
                    FROM jsonb_object_keys(issue.watcher_users) w
                ) ELSE TRUE END
            ORDER BY creation_time DESC
            LIMIT 1000
        """
        issues = self.__metadb.all(query, {
            "creation_time": creation_time,
            "modification_time": modification_time,
            "issue_type_id": issue_type_id,
            "issue_status_id": issue_status_id,
            "assignee_user_id": assignee_user_id,
            "reporter_user_id": reporter_user_id,
            "watcher_users": ",".join(map(str, watcher_users)) if watcher_users else None
        })
        return [IssueGetItem(**issue) for issue in issues]