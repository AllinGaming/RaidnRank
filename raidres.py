import pandas as pd

RAIDRES_PATH = "raidres.csv"
BABOONS_PATH = "baboons.csv"
OUTPUT_PATH = "finalized_raidres.csv"

# Load inputs
df = pd.read_csv(RAIDRES_PATH)
baboons = pd.read_csv(BABOONS_PATH)

# Only these ranks are eligible to be doubled.
eligible_ranks = {"Core Silverback", "Officer Wukong", "Wise Monkey"}
# Only these ranks are included in the finalized output.
included_ranks = eligible_ranks | {"Raider Gorilla"}
name_to_rank = baboons.set_index("name")["rank"]
df["rank"] = df["Attendee"].map(name_to_rank)

# Match 'x2' or '2x', case-insensitive, and apply rank gate.
mask_comment = df["Comment"].str.contains(r"\b(x2|2x)\b", case=False, na=False)
mask_eligible = df["rank"].isin(eligible_ranks)
mask_included = df["rank"].isin(included_ranks)

# Include only allowed ranks, and duplicate eligible rows with x2/2x.
df_included = df[mask_included]
df_doubled = pd.concat([df_included, df_included[mask_comment & mask_eligible]], ignore_index=True)
df_doubled = df_doubled.drop(columns=["rank"])

# Save the result
df_doubled.to_csv(OUTPUT_PATH, index=False)
print(f"Saved as {OUTPUT_PATH}")
