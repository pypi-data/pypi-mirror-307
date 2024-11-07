import pytest

from BdrcDbLib.DbOrm.DrsContextBase import DrsDbContextBase
from BdrcDbLib.DbOrm.models.drs import *


@pytest.mark.skip("in production")
def test_gb_ready_track():
    assert False


@pytest.mark.skip("in production")
def test_works():
    assert False


@pytest.mark.skip("in production")
def test_volumes():
    assert False


def test_gb_metadata():
    with DrsDbContextBase() as ctx:
        xx = ctx.session.query(GbMetadata).first()
        print(xx)


@pytest.mark.skip("in production")
def test_gb_content():
    assert False


@pytest.mark.skip("in production")
def test_gb_state():
    assert False


@pytest.mark.skip("in production")
def test_gb_download():
    assert False


@pytest.mark.skip("in production")
def test_gb_ready_track():
    assert False


@pytest.mark.skip("in production")
def test_gb_unpack():
    assert False


@pytest.mark.skip("in production")
def test_gb_distribution():
    assert False


def test_dip_activities_default_db():
    with DrsDbContextBase() as ctx:
        dbAx = ctx.session.query(DipActivities).all()
        assert dbAx

def test_dip_named_db_not_found():
    with pytest.raises(FileNotFoundError):
        with DrsDbContextBase('prod:notfoundfile') as ctx:
            dbAx = ctx.session.query(DipActivities).all()
            assert len(dbAx) > 3

            xxx = ctx.session.query(DipActivities.label).all()
            assert(len(xxx) > 3)

def test_dip_section_not_found():
    """
    Use an unknown section in a found file
    """
    with pytest.raises(KeyError):
        with DrsDbContextBase('notfoundsection:~/.config/bdrc/db_unit_test.config') as ctx:
            dbAx = ctx.session.query(DipActivities).all()
            assert len(dbAx) > 3

            xxx = ctx.session.query(DipActivities.label).all()
            assert(len(xxx) > 3)

def test_dip_named_db_found():
    with DrsDbContextBase('qa:~/.config/bdrc/db_unit_test.config') as ctx:
        dbAx = ctx.session.query(DipActivities).all()
        assert len(dbAx) > 3
        assert 'QA_TEST_ACTIVITY' in [x.label for x in dbAx]


def test_dip_named_db_found():
    """
    Requires you to define this section
    """
    with DrsDbContextBase('testprod:~/.config/bdrc/db_unit_test.config') as ctx:
        dbAx = ctx.session.query(DipActivities).all()
        print(dbAx)
        assert len(dbAx) > 3
        assert 'QA_TEST_ACTIVITY' not in [x.label for x in dbAx]