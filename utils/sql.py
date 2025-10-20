from sqlalchemy import text, select, insert, delete
from sqlalchemy.orm import Session


class sql:

    # Adds a static channel that users join to create a dynamic channel
    def Add_channel_Static(db, channel_id, debug=False):
        if debug:
            print(channel_id)
        try:
            session = Session(db)
            session.execute(
                text(
                    f"insert into channel_static (discord_channel_ID) values ('{channel_id}');"
                )
            )
            session.commit()
        except Exception as e:
            print(f"Error adding static channel: {e}")
            session.rollback()
            raise e
        finally:
            session.close()

    # Adds a Dynamic channel that users get moved to from a
    def Add_channel_Dynamic(db, channel_id, debug=False):
        if debug:
            print(channel_id)
        try:
            session = Session(db)
            session.execute(
                text(
                    f"insert into channel_dynamic (discord_channel_ID) values ('{channel_id}');"
                )
            )
            session.commit()
        except Exception as e:
            print(f"Error adding dynamic channel: {e}")
            session.rollback()
            raise e
        finally:
            session.close()

    # Deletes a static channel entry
    def Delete_channel_Static(db, channel_id, debug=False):
        if debug:
            print(channel_id)
        try:
            session = Session(db)
            session.execute(
                text(
                    f"delete from channel_static where discord_channel_ID = '{channel_id}';"
                )
            )
            session.commit()
        except Exception as e:
            print(f"Error deleting static channel: {e}")
            session.rollback()
            raise e
        finally:
            session.close()

    # Delete a Dynamic channel entry
    def Delete_channel_Dynamic(db, channel_id, debug=False):
        if debug:
            print(channel_id)
        try:
            session = Session(db)
            session.execute(
                text(
                    f"delete from channel_dynamic where discord_channel_ID = '{channel_id}';"
                )
            )
            session.commit()
        except Exception as e:
            print(f"Error deleting dynamic channel: {e}")
            session.rollback()
            raise e
        finally:
            session.close()

    # List all static channels
    def List_Channel_Static(db, debug=False):
        session = Session(db)
        channel_ID_List = (
            session.execute(text("select discord_channel_ID from channel_static;"))
            .scalars()
            .all()
        )
        if debug:
            print(f"Channel_list: {channel_ID_List}")
        session.close()
        return channel_ID_List

    # List all Dynamic channels
    def List_Channel_Dynamic(db, debug=False):
        session = Session(db)
        channel_ID_List = (
            session.execute(text("select discord_channel_ID from channel_dynamic;"))
            .scalars()
            .all()
        )
        if debug:
            print(f"Channel_list: {channel_ID_List}")
        session.close()
        return channel_ID_List

    # Check if a channel is registered as Static
    def is_Channel_Static(db, channel_id, debug=False):
        session = Session(db)
        result = session.execute(
            text(
                f"select exists (select 1 from channel_static where discord_channel_ID = '{channel_id}');"
            )
        ).scalar()
        if debug:
            print(f"Is Channel Static: {result}")
        session.close()
        return result

    # Check if a channel is registered as Dynamic
    def is_channel_Dynamic(db, channel_id, debug=False):
        session = Session(db)
        result = session.execute(
            text(
                f"select exists (select 1 from channel_dynamic where discord_channel_ID = '{channel_id}');"
            )
        ).scalar()
        if debug:
            print(f"Is Channel Dynamic: {result}")
        session.close()
        return result
