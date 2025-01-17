from uuid import UUID
from typing import List
from abc import ABC, abstractmethod

from app.domain.entities import Group, Student


class BaseGroupPersistence(ABC):
    @abstractmethod
    def get_by_id(self, group_id: UUID) -> Group | None:
        """Get group by ID"""
        ...

    @abstractmethod
    def get_all(self) -> List[Group]:
        """Get all groups"""
        ...

    @abstractmethod
    def create_group(self, group: Group) -> Group:
        """Create new group"""
        ...

    @abstractmethod
    def delete_group(self, group_id: UUID) -> None:
        """Delete group"""
        ...

    @abstractmethod
    def get_all_students(self) -> List[Student]:
        """Get all students"""
        ...

    @abstractmethod
    def get_student_by_id(self, student_id: UUID) -> Student | None:
        """Get student by ID"""
        ...

    @abstractmethod
    def create_student(self, student: Student) -> Student:
        """Create new student"""
        ...

    @abstractmethod
    def delete_student(self, student_id: UUID) -> None:
        """Delete student"""
        ...

    @abstractmethod
    def get_group_students(self, group_id: UUID) -> List[Student]:
        """Get all students in a group"""
        ...

    @abstractmethod
    def assign_student_to_group(self, student_id: UUID, group_id: UUID) -> None:
        """Assign student to group"""
        ...

    @abstractmethod
    def remove_student_from_group(self, student_id: UUID, group_id: UUID) -> None:
        """Remove student from group"""
        ...

    @abstractmethod
    def transfer_student_between_groups(self, student_id: UUID, from_group_id: UUID, to_group_id: UUID) -> None:
        """Transfer student from one group to another"""
        ...
