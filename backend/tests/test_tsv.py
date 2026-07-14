from app.models.note import Note
from app.models.user import User

def test_tsv_populates_on_insert(db_session):
    user = User(email="tsv@test.com", password_hash="x")
    db_session.add(user)
    db_session.flush()

    note = Note(user_id=user.id, title="Running notes", body="Search is fast")
    db_session.add(note)
    db_session.commit()
    db_session.refresh(note)

    assert note.tsv is not None
    assert "'run'" in str(note.tsv)
    assert "'fast'" in str(note.tsv)