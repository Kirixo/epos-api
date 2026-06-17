from __future__ import annotations

from sqlalchemy.orm import Session

from app.domain.access.user_access_repository_protocol import UserWorkspaceAccessRepositoryProtocol
from app.domain.crud.crud_repository_protocol import CrudRepositoryProtocol
from app.domain.user.user_repository_protocol import UserRepositoryProtocol


"""
Воно поивнно повертати вже готові репозиторії а не їх  протоколи.

Умовно у нас 2 бази даних, одна із них чисто під юзерів (погстгрес)
а друга чисто під дані (монго). Тоді буде 2 теки в яких будуть 
реалізації цих репозиторіїв, а протокли (умовні інтерфейси) для
них будуть спільні. А ось оцей завод це буде збірка солянка чисто 
для UoW, ну в нашому випадку це буде год обжект для зв'язку з данними, фігня
-- да, розумію, а ти хочеш думатаи більше і пробити під кожен сервіс/группу сервісів
свій UoW? А Unit of Work такий цікавий патерн, хоч і він реалізвоаний в деяких фреймворках для спілкеування з бд
але краще мати ще один звреху тіпа як декоратор, бо бог знає що воно може накоїти та можуть бути свої
реалізації для цього. як в нашому випадку може знадобитися UoW 
з репозиторіями чисто під резолвінг конфліктів в якому вде реалізована механіка 
того як їх резолвить, а зверху це буде просто репозиторії зі збреженням. Ну корчое почиатй та потруси геміні
"""


class GeneralRepositoriesFactory:
    def workspace_access_repo(self, session: Session) -> UserWorkspaceAccessRepositoryProtocol:
        raise NotImplementedError
    
    def crud_repository(self, session: Session) ->  CrudRepositoryProtocol:
        raise NotImplementedError
        
    def user_repository(self, session: Session) -> UserRepositoryProtocol:
        raise NotImplementedError