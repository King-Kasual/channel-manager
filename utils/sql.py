from sqlalchemy import text, select
from sqlalchemy.orm import Session


class sql:

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
        session = Session(db)
        channel_ID_List = (
            session.execute(text("select discord_channel_ID from channel_static;"))
            .scalars()
            .all()
        )
        print(f"Channel_list: {channel_ID_List}")
        return channel_ID_List

    def List_Channel_Dynamic(db):
        session = Session(db)
        channel_ID_List = (
            session.execute(text("select discord_channel_ID from channel_dynamic;"))
            .scalars()
            .all()
        )
        print(f"Channel_list: {channel_ID_List}")
        return channel_ID_List
