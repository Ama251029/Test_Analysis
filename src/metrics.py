import pandas as pd

def summarize_numeric(series):

    return pd.Series({
        "count": series.count(),
        "mean": series.mean(),
        "median": series.median(),
        "min": series.min(),
        "p25": series.quantile(0.25),
        "p75": series.quantile(0.75),
        "max": series.max(),
    })

def build_conversation_dataset(interaction_df):

    df = interaction_df.sort_values(
        ["chatId", "interactionCount", "timestamp"]
    ).copy()

    conversation_df = (
        df.groupby("chatId")
        .agg(
            userId=("userId", "first"),

            first_timestamp=("timestamp", "min"),
            last_timestamp=("timestamp", "max"),

            observed_interaction_count=("chatId", "size"),
            active_days=("interaction_date", "nunique"),

            # 노트북 작동을 위한 원본 데이터 보존
            chatTotalInteractionCount=("chatTotalInteractionCount", "first"),
        )
        .reset_index()
    )

    # Conversation span
    conversation_df["conversation_span_minutes"] = (
        (
            conversation_df["last_timestamp"]
            - conversation_df["first_timestamp"]
        )
        .dt.total_seconds()
        / 60
    )

    # Conversation type
    conversation_df["is_multi_turn"] = (
        conversation_df["observed_interaction_count"] >= 2
    )

    conversation_df["is_multi_day"] = (
        conversation_df["active_days"] >= 2
    )

    # 첫 interaction
    first_interaction = df[
    df["observed_interaction_index"] == 0
].copy()

    first_features = first_interaction[
        [
            "chatId",
            "intent",
            "intent_category",
            "intent_subcategory",
            "prompt_char_count",
            "response_char_count",
        ]
    ].rename(
        columns={
            "intent": "first_intent",
            "intent_category": "first_intent_category",
            "intent_subcategory": "first_intent_subcategory",
            "prompt_char_count": "first_prompt_char_count",
            "response_char_count": "first_response_char_count",
        }
    )

    conversation_df = conversation_df.merge(
        first_features,
        on="chatId",
        how="left",
    )

    return conversation_df

def build_user_dataset(interaction_df, conversation_df):

    df = interaction_df.copy()

    user_df = (
        df.groupby("userId")
        .agg(
            first_timestamp=("timestamp", "min"),
            last_timestamp=("timestamp", "max"),
            conversation_count=("chatId", "nunique"),
            interaction_count=("chatId", "size"),
            active_days=("interaction_date", "nunique"),
        )
        .reset_index()
    )

    user_df["is_returning"] = (
        user_df["active_days"] >= 2
    )

    # 최초 활동일
    first_dates = (
        df.groupby("userId")["interaction_date"]
        .min()
        .rename("first_active_date")
    )

    df = df.merge(
        first_dates,
        on="userId",
        how="left",
    )

    first_day_df = df[
        df["interaction_date"] == df["first_active_date"]
    ]

    first_day_metrics = (
        first_day_df.groupby("userId")
        .agg(
            first_day_conversation_count=("chatId", "nunique"),
            first_day_interaction_count=("chatId", "size"),
        )
        .reset_index()
    )

    user_df = user_df.merge(
        first_day_metrics,
        on="userId",
        how="left",
    )

    # 사용자별 첫 conversation
    first_chat = (
        conversation_df
        .sort_values(["userId", "first_timestamp", "chatId"])
        .groupby("userId")
        .first()
        .reset_index()
    )

    first_chat_features = first_chat[
        [
            "userId",
            "observed_interaction_count",
            "chatTotalInteractionCount",
            "is_multi_turn",
            "first_intent",
            "first_intent_category",
            "first_intent_subcategory",
            "first_prompt_char_count",
        ]
    ].rename(
        columns={
            "observed_interaction_count": "first_chat_interaction_count",
            "is_multi_turn": "first_chat_is_multi_turn",
        }
    )

    user_df = user_df.merge(
        first_chat_features,
        on="userId",
        how="left",
    )

    # 두 번째 활동일까지 걸린 기간
    active_dates = (
        df[["userId", "interaction_date"]]
        .drop_duplicates()
        .sort_values(["userId", "interaction_date"])
    )

    active_dates["active_day_order"] = (
        active_dates.groupby("userId")
        .cumcount()
    )

    second_dates = (
        active_dates[
            active_dates["active_day_order"] == 1
        ][["userId", "interaction_date"]]
        .rename(
            columns={
                "interaction_date": "second_active_date"
            }
        )
    )

    user_df = user_df.merge(
        first_dates.reset_index(),
        on="userId",
        how="left",
    )

    user_df = user_df.merge(
        second_dates,
        on="userId",
        how="left",
    )

    user_df["days_to_second_active_day"] = (
        pd.to_datetime(user_df["second_active_date"])
        - pd.to_datetime(user_df["first_active_date"])
    ).dt.days

    return user_df