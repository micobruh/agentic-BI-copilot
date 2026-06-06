from langgraph.checkpoint.sqlite import SqliteSaver


def get_checkpointer():
    return SqliteSaver.from_conn_string("bi_copilot_state.db")