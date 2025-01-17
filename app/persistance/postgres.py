from uuid import UUID
from typing import List
from sqlmodel import Session, select

from app.db.models import GroupModel, StudentModel, GroupStudentModel
from app.domain.entities import Group, Student
from app.persistance.base import BaseGroupPersistence


class PostgresGroupPersistence(BaseGroupPersistence):
    def __init__(self, session: Session):
        self.__session = session

    def get_by_id(self, group_id: UUID) -> Group | None:
        """Get group by ID"""
        query = select(GroupModel).where(GroupModel.id == group_id)
        group = self.__session.exec(query).first()
        if group:
            return Group(id=group.id, name=group.name, number=group.group_number)
        return None

    def get_all(self) -> List[Group]:
        """Get all groups"""
        query = select(GroupModel)
        groups = self.__session.exec(query).all()
        return [
            Group(id=group.id, name=group.name, number=group.group_number)
            for group in groups
        ]

    def create_group(self, group: Group) -> Group:
        """Create new group"""
        db_group = GroupModel(
            id=group.id,
            name=group.name,
            group_number=group.number,
        )
        self.__session.add(db_group)
        self.__session.commit()
        self.__session.refresh(db_group)
        return Group(id=db_group.id, name=db_group.name, number=db_group.group_number)

    def delete_group(self, group_id: UUID) -> None:
        """Delete group"""
        # First delete group-student relationships
        query = select(GroupStudentModel).where(GroupStudentModel.group_id == group_id)
        relations = self.__session.exec(query).all()
        for relation in relations:
            self.__session.delete(relation)

        # Then delete the group
        query = select(GroupModel).where(GroupModel.id == group_id)
        group = self.__session.exec(query).first()
        if group:
            self.__session.delete(group)
            self.__session.commit()

    def get_all_students(self) -> List[Student]:
        """Get all students"""
        query = select(StudentModel)
        students = self.__session.exec(query).all()
        return [
            Student(id=student.id, name=student.name, number=student.student_number)
            for student in students
        ]

    def get_student_by_id(self, student_id: UUID) -> Student | None:
        """Get student by ID"""
        query = select(StudentModel).where(StudentModel.id == student_id)
        student = self.__session.exec(query).first()
        if student:
            return Student(id=student.id, name=student.name, number=student.student_number)
        return None

    def create_student(self, student: Student) -> Student:
        """Create new student"""
        db_student = StudentModel(
            id=student.id,
            name=student.name,
            student_number=student.number
        )
        self.__session.add(db_student)
        self.__session.commit()
        self.__session.refresh(db_student)
        return Student(id=db_student.id, name=db_student.name, number=db_student.student_number)

    def delete_student(self, student_id: UUID) -> None:
        """Delete student"""
        # First delete student-group relationships
        query = select(GroupStudentModel).where(GroupStudentModel.student_id == student_id)
        relations = self.__session.exec(query).all()
        for relation in relations:
            self.__session.delete(relation)

        # Then delete the student
        query = select(StudentModel).where(StudentModel.id == student_id)
        student = self.__session.exec(query).first()
        if student:
            self.__session.delete(student)
            self.__session.commit()

    def get_group_students(self, group_id: UUID) -> List[Student]:
        """Get all students in a group"""
        # Use join query to get all students in the group
        query = (
            select(StudentModel)
            .join(GroupStudentModel)
            .where(GroupStudentModel.group_id == group_id)
        )
        students = self.__session.exec(query).all()
        return [
            Student(id=student.id, name=student.name, number=student.student_number)
            for student in students
        ]

    def assign_student_to_group(self, student_id: UUID, group_id: UUID) -> None:
        """Assign student to group"""
        # Check if relationship already exists
        query = select(GroupStudentModel).where(
            (GroupStudentModel.student_id == student_id) &
            (GroupStudentModel.group_id == group_id)
        )
        existing = self.__session.exec(query).first()

        if not existing:
            # Create new relationship
            relation = GroupStudentModel(student_id=student_id, group_id=group_id)
            self.__session.add(relation)
            self.__session.commit()

    def remove_student_from_group(self, student_id: UUID, group_id: UUID) -> None:
        """Remove student from group"""
        query = select(GroupStudentModel).where(
            (GroupStudentModel.student_id == student_id) &
            (GroupStudentModel.group_id == group_id)
        )
        relation = self.__session.exec(query).first()
        if relation:
            self.__session.delete(relation)
            self.__session.commit()

    def transfer_student_between_groups(self, student_id: UUID, from_group_id: UUID, to_group_id: UUID) -> None:
        """Transfer student from one group to another"""
        # Remove from original group
        self.remove_student_from_group(student_id, from_group_id)
        # Add to new group
        self.assign_student_to_group(student_id, to_group_id)
