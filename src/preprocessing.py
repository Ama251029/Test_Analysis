import pandas as pd


def parse_llm_label(value):
    """llm_label에서 분석용 필드를 추출한다."""

    if not isinstance(value, dict):
        return pd.Series({
            "intent": None,
            "intent_category": None,
            "intent_subcategory": None,
            "intent_justification": None,
        })

    label = value.get("label")
    justification = value.get("justification")

    category = None
    subcategory = None

    if isinstance(label, str):
        parts = label.split(">", maxsplit=1)

        category = parts[0].strip()

        if len(parts) == 2:
            subcategory = parts[1].strip()

    return pd.Series({
        "intent": label,
        "intent_category": category,
        "intent_subcategory": subcategory,
        "intent_justification": justification,
    })


def build_interaction_dataset(df):
    """원본 데이터를 interaction 단위 분석 데이터로 변환한다."""

    interaction_df = df.copy()

    # 시간
    interaction_df["timestamp"] = pd.to_datetime(
        interaction_df["timestamp"],
        errors="coerce",
    )

    interaction_df["chatStartTime"] = pd.to_datetime(
        interaction_df["chatStartTime"],
        errors="coerce",
    )

    interaction_df["interaction_date"] = (
        interaction_df["timestamp"].dt.date
    )

    # 관측 순서 재정의
    interaction_df = interaction_df.sort_values(
        ["chatId", "timestamp"]
    ).copy()

    interaction_df["observed_interaction_index"] = (
        interaction_df.groupby("chatId")
        .cumcount()
    )
    
    interaction_df["interaction_hour"] = (
        interaction_df["timestamp"].dt.hour
    )

    # llm_label
    label_df = interaction_df["llm_label"].apply(parse_llm_label)

    interaction_df = pd.concat(
        [interaction_df, label_df],
        axis=1,
    )

    # 텍스트 길이
    interaction_df["prompt_char_count"] = (
        interaction_df["prompt"]
        .fillna("")
        .str.len()
    )

    interaction_df["prompt_word_count"] = (
        interaction_df["prompt"]
        .fillna("")
        .str.split()
        .str.len()
    )

    interaction_df["response_char_count"] = (
        interaction_df["response"]
        .fillna("")
        .str.len()
    )

    return interaction_df