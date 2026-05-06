from typing import Optional
import datetime
import enum

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    Enum,
    ForeignKeyConstraint,
    Identity,
    Integer,
    PrimaryKeyConstraint,
    String,
    Text,
    Time,
    UniqueConstraint,
    text,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Gender(str, enum.Enum):
    MALE = "Male"
    FEMALE = "Female"


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    SUPERVISOR = "supervisor"
    TEACHER = "teacher"


class Parents(Base):
    __tablename__ = "parents"
    __table_args__ = (PrimaryKeyConstraint("id", name="parents_pkey"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)

    students: Mapped[list["Students"]] = relationship(
        "Students", back_populates="parent"
    )


class Staff(Base):
    __tablename__ = "staff"
    __table_args__ = (
        ForeignKeyConstraint(
            ["supervisor_id"], ["staff.id"], name="staff_supervisor_id_fkey"
        ),
        PrimaryKeyConstraint("id", name="staff_pkey"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(
        Enum(
            UserRole,
            values_callable=lambda cls: [member.value for member in cls],
            name="user_role",
        ),
        nullable=False,
    )
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    birth_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    gender: Mapped[Optional[Gender]] = mapped_column(
        Enum(
            Gender,
            values_callable=lambda cls: [member.value for member in cls],
            name="gender",
        )
    )
    quran_memorization: Mapped[Optional[str]] = mapped_column(Text)
    ijazah: Mapped[Optional[str]] = mapped_column(Text)
    supervisor_id: Mapped[Optional[int]] = mapped_column(Integer)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime, server_default=text("CURRENT_TIMESTAMP")
    )

    supervisor: Mapped[Optional["Staff"]] = relationship(
        "Staff", remote_side=[id], back_populates="supervisor_reverse"
    )
    supervisor_reverse: Mapped[list["Staff"]] = relationship(
        "Staff", remote_side=[supervisor_id], back_populates="supervisor"
    )
    students: Mapped[list["Students"]] = relationship(
        "Students", back_populates="teacher"
    )
    reports: Mapped[list["Reports"]] = relationship("Reports", back_populates="teacher")
    schedules: Mapped[list["Schedules"]] = relationship(
        "Schedules", back_populates="staff"
    )


class Students(Base):
    __tablename__ = "students"
    __table_args__ = (
        ForeignKeyConstraint(
            ["parent_id"],
            ["parents.id"],
            ondelete="SET NULL",
            name="students_parent_id_fkey",
        ),
        ForeignKeyConstraint(
            ["teacher_id"],
            ["staff.id"],
            ondelete="SET NULL",
            name="students_teacher_id_fkey",
        ),
        PrimaryKeyConstraint("id", name="students_pkey"),
        UniqueConstraint("email", name="email_uq"),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(
            start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1
        ),
        primary_key=True,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    birth_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    gender: Mapped[Optional[Gender]] = mapped_column(
        Enum(
            Gender,
            values_callable=lambda cls: [member.value for member in cls],
            name="gender",
        )
    )
    quran_progress: Mapped[Optional[str]] = mapped_column(Text)
    monthly_package: Mapped[Optional[str]] = mapped_column(String(100))
    parent_id: Mapped[Optional[int]] = mapped_column(Integer)
    teacher_id: Mapped[Optional[int]] = mapped_column(Integer)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime, server_default=text("CURRENT_TIMESTAMP")
    )

    parent: Mapped[Optional["Parents"]] = relationship(
        "Parents", back_populates="students"
    )
    teacher: Mapped[Optional["Staff"]] = relationship(
        "Staff", back_populates="students"
    )
    reports: Mapped[list["Reports"]] = relationship("Reports", back_populates="student")
    schedules: Mapped[list["Schedules"]] = relationship(
        "Schedules", back_populates="student"
    )


class Reports(Base):
    __tablename__ = "reports"
    __table_args__ = (
        ForeignKeyConstraint(
            ["student_id"],
            ["students.id"],
            ondelete="CASCADE",
            name="reports_student_id_fkey",
        ),
        ForeignKeyConstraint(
            ["teacher_id"],
            ["staff.id"],
            ondelete="SET NULL",
            name="reports_teacher_id_fkey",
        ),
        PrimaryKeyConstraint("id", name="reports_pkey"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    teacher_id: Mapped[int] = mapped_column(Integer, nullable=False)
    student_id: Mapped[int] = mapped_column(Integer, nullable=False)
    report_text: Mapped[str] = mapped_column(Text, nullable=False)
    quran_reached: Mapped[Optional[str]] = mapped_column(Text)
    evaluation_grade: Mapped[Optional[str]] = mapped_column(String(50))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime, server_default=text("CURRENT_TIMESTAMP")
    )

    student: Mapped["Students"] = relationship("Students", back_populates="reports")
    teacher: Mapped["Staff"] = relationship("Staff", back_populates="reports")


class Schedules(Base):
    __tablename__ = "schedules"
    __table_args__ = (
        ForeignKeyConstraint(
            ["staff_id"],
            ["staff.id"],
            ondelete="CASCADE",
            name="schedules_staff_id_fkey",
        ),
        ForeignKeyConstraint(
            ["student_id"],
            ["students.id"],
            ondelete="CASCADE",
            name="schedules_student_id_fkey",
        ),
        PrimaryKeyConstraint("id", name="schedules_pkey"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(Integer, nullable=False)
    staff_id: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[Optional[datetime.time]] = mapped_column(Time)
    end_time: Mapped[Optional[datetime.time]] = mapped_column(Time)
    sat: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text("false"))
    sun: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text("false"))
    mon: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text("false"))
    tues: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text("false"))
    wednes: Mapped[Optional[bool]] = mapped_column(
        Boolean, server_default=text("false")
    )
    thurs: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text("false"))
    fri: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text("false"))

    staff: Mapped["Staff"] = relationship("Staff", back_populates="schedules")
    student: Mapped["Students"] = relationship("Students", back_populates="schedules")
