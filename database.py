def init_db():

    import os

    if os.path.exists("ev_saas.db"):
        os.remove("ev_saas.db")

    Base.metadata.create_all(engine)
