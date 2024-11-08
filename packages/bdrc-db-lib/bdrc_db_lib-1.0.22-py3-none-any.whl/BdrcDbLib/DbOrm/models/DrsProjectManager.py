#!/usr/bin/env python3
"""
DRS Database elements supporting projects.
When done, import into BdrcDbLib.DbOrm.models.drs
from AO Dashboard #1 (https://github.com/buda-base/ao-dashboard/issues/1)

"""
from BdrcDbLib.DbOrm.DrsContextBase import DrsDbContextBase
from BdrcDbLib.DbOrm.models.drs import Base, IdTimestampMixin, TimestampMixin
from sqlalchemy import Column, text
from sqlalchemy import ForeignKey, String, Integer
from sqlalchemy.dialects.mysql import (
    # BINARY,
    # BIT,
    # BLOB,
    # BOOLEAN,
    # CHAR,
    # DATE,
    # DATETIME,
    # DECIMAL,
    # DECIMAL,
    # DOUBLE,
    # ENUM,
    # FLOAT,
    # INTEGER,
    # LONGBLOB,
    LONGTEXT,
    # MEDIUMBLOB,
    # MEDIUMINT,
    # MEDIUMTEXT,
    # NCHAR,
    # NUMERIC,
    # NVARCHAR,
    # REAL,
    # SET,
    # SMALLINT,
    # TEXT,
    # TIME,
    # TINYBLOB,
    # TINYINT,
    # TINYTEXT,
    # VARBINARY,
    # VARCHAR,
    # YEAR,
    TIMESTAMP
)
from sqlalchemy.orm import relationship

#region initial data

project_types: [{}] = [
    {"name": "Acquisition", "desc": "Projects that assess and acquire"},
    {"name": "Processing", "desc": "Image preparation"},
    {"name": "Distribution", "desc": "Distribution"}
]

member_types: [] = [
    "Work",
    "Volume"
]

member_states: [{}] = [
    {"name": "Not started", "desc":"" },
    {"name": "In process", "desc":"" },
    {"name": "Complete", "desc":"" }
]
#endregion

# Base = declarative_base()


class ProjectTypes(IdTimestampMixin, Base):
    """
    enum
    Initial data:
    Acquisition
    Processing
    Distribution
    """
    __tablename__ = "pm_project_types"
    project_type_name = Column(String(45), nullable=False)
    project_type_desc = Column(LONGTEXT)

    project = relationship("Projects", back_populates="project_type")

    def __repr__(self):
        return f"<{self.id}: {self.project_type_name}>"


class Projects(IdTimestampMixin, Base):
    """
    Timestamp mixin has the PK
    """
    __tablename__ = "pm_projects"
    name = Column(String(45))
    description = Column(LONGTEXT)

    project_type_id = Column(Integer, ForeignKey('pm_project_types.id'))
    project_type = relationship("ProjectTypes",back_populates="project")

    m_type_id = Column(Integer, ForeignKey('pm_member_types.id'))
    m_type = relationship("MemberTypes", back_populates="project")

    member = relationship("ProjectMembers", back_populates="project")

    # steps = relationship("ProjectSteps", back_populates="project")

    def __repr__(self):
        return f"<{self.id}: {self.name}-{self.project_type}-{self.m_type}>"


class MemberTypes(IdTimestampMixin, Base):
    """
    enum
    Initial data:
    work
    volume
    """
    __tablename__ = "pm_member_types"
    m_type = Column(String(45), nullable=False)
    project = relationship('Projects', back_populates='m_type')
    members = relationship("ProjectMembers", back_populates="member_type")

    def __repr__(self):
        return f"<{self.id}: {self.m_type}>"


class MemberStates(IdTimestampMixin, Base):
    """
    enum
    Initial data:
    not_started
    in_progress
    complete
    """
    __tablename__ = "pm_member_states"
    m_state_name = Column(String(45), nullable=False)
    m_state_desc = Column(LONGTEXT)

    project_member = relationship('ProjectMembers', back_populates="project_member_state")

    def __repr__(self):
        return f"<{self.id}: {self.m_state_name}>"


class ProjectMembers(TimestampMixin, Base):
    """
    State of each member in a project.
    PK
    """
    __tablename__ = "pm_project_members"
    pm_id = Column(Integer, primary_key=True, autoincrement=True)
    pm_type = Column(Integer, ForeignKey('pm_member_types.id'))

    # Put in relationships when move into drs model
    pm_work_id = Column(Integer, ForeignKey('Works.workId'))
    pm_volume_id = Column(Integer, ForeignKey('Volumes.volumeId'))
    #
    pm_project = Column(Integer, ForeignKey('pm_projects.id'))
    project = relationship("Projects", back_populates="member")

    pm_project_state_id = Column(Integer, ForeignKey('pm_member_states.id'))

    member_type = relationship("MemberTypes", back_populates="members")
    project_member_state = relationship('MemberStates', back_populates="project_member")

    def __repr__(self):
        return f"<{self.pm_id}: {self.project} {self.member_type} {self.project_state}>"

class Steps(IdTimestampMixin, Base):
    """
    Abstract project steps. Associated with a project through
    the many to many ProjectSteps
    """
    __tablename__ = "pm_steps"
    s_name = Column(String(45), nullable=False)
    s_desc = Column(LONGTEXT)


class ProjectSteps(IdTimestampMixin, Base):
    """
    Many to many project to step relationships
    """
    __tablename__ = "pm_project_steps"
    ps_project = Column(ForeignKey('Projects.id'))

    # project = relationship("Projects", back_populates="steps")
    # membersteps = relationship("ProjectMemberSteps", back_populates="projectstep")


class ProjectMemberSteps(TimestampMixin, Base):
    """
    Journal of each project member's transition through a state
    """
    __tablename__ = "pm_project_member_steps"
    project_member_id = Column(ForeignKey('ProjectMembers.pm_id'), primary_key=True)
    project_step_id = Column(ForeignKey("ProjectSteps.id"), primary_key=True)
    project_step_time = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))

    # projectstep = relationship('Projects', back_populates='membersteps')
    # membersteps = relationship('ProjectSteps', back_populates='steps')
    # member = relationship('ProjectMembers', back_populates='steps')



def create_tables():
    with DrsDbContextBase() as drs:
        bobby_tables: [] = [
            Projects().__table__,
            ProjectTypes().__table__,
            MemberTypes().__table__,
            MemberStates().__table__,
            ProjectMembers().__table__,
        ]

        Base.metadata.create_all(drs.get_engine(), checkfirst=True, tables=bobby_tables)


def initial_data():
    """
    Populate tables
    :return:
    """
    with DrsDbContextBase() as drs:
        # If these tables existed before, truncate them
        trunc_tables: [] = [
            Projects,
            ProjectTypes,
            MemberTypes,
            MemberStates,
            ProjectMembers
        ]
        # zz = [drs.session.query(x).delete() for x in trunc_tables]

        for pt in project_types:
            drs.session.add(ProjectTypes(project_type_name=pt["name"], project_type_desc=pt["desc"]))

        for mt in member_types:
            drs.session.add(MemberTypes(m_type=mt))

        for ms in member_states:
            drs.session.add(MemberStates(m_state_name=ms["name"], m_state_desc=ms["desc"]))

        drs.session.commit()

    dd = drs.session.query(MemberStates).all()
    print(dd)

    dd = drs.session.query(MemberTypes).all()
    print(dd)

    dd = drs.session.query(ProjectTypes).all()
    print(dd)


if __name__ == '__main__':
    create_tables()
    initial_data()


