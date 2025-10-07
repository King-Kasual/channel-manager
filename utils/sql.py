from sqlalchemy import text
from sqlalchemy.orm import Session


class sql:
    """def Setup_DB(db):
    if not sql.dialect.has_table(db, table_name):
        None
    """

    # Adds a static channel that users join to create a dynamic channel
    def Add_channel_Static(db, channel_id):
        session = Session(db)
        print(channel_id)
        session.execute(
            text(
                f"insert into channel_static (discord_channel_ID) values ('{channel_id}');"
            )
        )
        session.commit()

    # Adds a Dynamic channel that users get moved to from a
    def Add_channel_Dynamic(db, channel_id):
        session = Session(db)
        print(channel_id)
        session.execute(
            text(
                f"insert into channel_dynamic (discord_channel_ID) values ('{channel_id}');"
            )
        )
        session.commit()

    def Delete_channel_Static(db, channel_id):
        session = Session(db)
        print(channel_id)
        session.execute(
            text(
                f"delete from channel_static where discord_channel_ID = '{channel_id}';"
            )
        )
        session.commit()

    def Delete_channel_Dynamic(db, channel_id):
        session = Session(db)
        print(channel_id)
        session.execute(
            text(
                f"delete from channel_dynamic where discord_channel_ID = '{channel_id}';"
            )
        )
        session.commit()

    def List_Channel_Static(db):
        print("")
