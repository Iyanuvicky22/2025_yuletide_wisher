"""
Pass
"""
import os
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI
from yul_logger import logger

load_dotenv()

client = OpenAI(api_key=os.getenv("openai_key"))

PROMPT_TEMPLATE = """
You are writing a short, personalised festive message.

CONTEXT
Occasion: Christmas
Relationship to sender: {relationship_category}
Tone: {tone}
Additional_info: {additional_notes}

RECIPIENT
Name: {name}

STYLE RULES (IMPORTANT)
- Do NOT reuse common festive clichés.
- Use natural, varied phrasing.
- Keep it concise: 3–4 sentences maximum.
- Avoid emojis unless explicitly requested.

Write the message now.
""".strip()


def df_read_clean(file_path: str):
    """
    Custom function to read and clean
    the collated google form responses.

    Args:
        file_path (str): csv data file path.

    Returns:
        df: cleaned pandas dataframe.
    """

    df = pd.read_csv(file_path)

    new_cols = ["timestamp", "first_name", "surname", "alias",
                "email", "phone_no", "birthday", "relationship_category",
                "additional_notes"]
    df.columns = new_cols

    df["full_name"] = df['first_name']\
        .str.strip() + " " + df['surname'].str.strip()
    df["full_name"] = df["full_name"].str.lower().str.title()

    return df


def make_message(
    name: str,
    additional_notes: str = "",
    relationship_category: str = "friend",
    tone: str = "warm",
) -> str:
    """
    ChatGPT custom function to generated text based
    on *args from the collated data.
    Args:
        name (str): name of person.
        additional_notes (str, optional): personal notes to highlight person's
            relationship. Defaults to "".
        relationship_category (str, optional): category of person's
            relationship with me. Defaults to "friend".
        tone (str, optional): tone of text outputs. Defaults to "warm".

    Returns:
        str: generated text.
    """
    prompt = PROMPT_TEMPLATE.format(
        name=name,
        relationship_category=relationship_category,
        tone=tone,
        additional_notes=additional_notes,
    )

    resp = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
    )
    return resp.output_text.strip()


def message_main():
    """
    main function to run all custom functions and
    generate a new output file with generated text in
    it's column.
    """
    input_csv = r"data\responses.csv"
    output_file = r"data\responses_with_ai.xlsx"

    df = df_read_clean(input_csv)

    name_col = "first_name"
    email_col = "email"
    notes_col = "additional_notes"
    relationship_col = "relationship_category"
    tone_col = "tone"

    if "ai_message" not in df.columns:
        df["ai_message"] = ""

    for i, row in df.iterrows():
        name = str(row.get(name_col, "")).strip()
        email = str(row.get(email_col, "")).strip()

        if not name or not email:
            continue

        if isinstance(row["ai_message"], str) and row["ai_message"].strip():
            continue

        additional_notes = str(row.get(notes_col, "")).strip()
        relationship = str(row.get(relationship_col, "friend")).strip()
        tone = str(row.get(tone_col, "warm")).strip()

        try:
            df.at[i, "ai_message"] = make_message(
                name=name,
                additional_notes=additional_notes,
                relationship_category=relationship,
                tone=tone,
            )
            logger.info("%s Generated for: %s", name, tone)
        except Exception as e:
            df.at[i, "ai_message"] = f"ERROR: {e}"
            logger.error("%s Failed for %s", name, e)

    df.to_excel(output_file, index=False, engine="openpyxl")
    logger.info("%s \nSaved: %s", output_file, "oya-na")


if __name__ == "__main__":
    message_main()
