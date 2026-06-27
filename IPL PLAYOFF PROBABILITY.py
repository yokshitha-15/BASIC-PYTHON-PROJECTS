# Current points table before the remaining matches.
# We keep the original order to break ties in a simple, predictable way.
teams = [
    {"team": "RCB", "pts": 18},
    {"team": "GT", "pts": 16},
    {"team": "SRH", "pts": 16},
    {"team": "RR", "pts": 14},
    {"team": "PBKS", "pts": 13},
    {"team": "KKR", "pts": 13},
    {"team": "CSK", "pts": 12},
    {"team": "DC", "pts": 12},
    {"team": "MI", "pts": 8},
    {"team": "LSG", "pts": 8},
]

# Remaining fixtures. Each match can be won by either team.
fixtures = [
    ("GT", "CSK"),
    ("SRH", "RCB"),
    ("LSG", "PBKS"),
    ("MI", "RR"),
    ("KKR", "DC"),
]

# This dictionary helps us preserve the original order during point ties.
team_order = {team["team"]: index for index, team in enumerate(teams)}

# This dictionary stores how many final tables each team qualifies in.
qualify_count = {team["team"]: 0 for team in teams}

# This list stores all 32 final tables.
all_final_tables = []

def sort_points_table(num_of_points):
    """Sort teams by points. If points are tied, keep original table order."""
    return sorted(
        num_of_points.items(),
        key=lambda item: (-item[1], team_order[item[0]])
    )

def simulate_matches(match_index, num_of_points, winner_path):
    """
    Recursively simulate every possible match result.

    Example:
    Match 1 has 2 branches.
    Match 2 doubles those into 4 branches.
    Match 3 doubles those into 8 branches.
    After 5 matches, we get 32 final tables.
    """

    # If all matches are simulated, create one final points table.
    if match_index == len(fixtures):
        sorted_table = sort_points_table(num_of_points)
        top_4 = [team for team, pts in sorted_table[:4]]

        # Count one qualification for every team in the top 4.
        for team in top_4:
            qualify_count[team] += 1

        # Save this final table so we can print it later.
        all_final_tables.append({
            "winner_path": winner_path,
            "table": sorted_table,
            "top_4": top_4,
        })
        return

    team_1, team_2 = fixtures[match_index]

    # Branch 1: team_1 wins this match.
    points_if_team_1_wins = num_of_points.copy()
    points_if_team_1_wins[team_1] += 2
    simulate_matches(
        match_index + 1,
        points_if_team_1_wins,
        winner_path + [team_1]
    )

    # Branch 2: team_2 wins this match.
    points_if_team_2_wins = num_of_points.copy()
    points_if_team_2_wins[team_2] += 2
    simulate_matches(
        match_index + 1,
        points_if_team_2_wins,
        winner_path + [team_2]
    )


# Start with the current points before any remaining match is played.
starting_points = {team["team"]: team["pts"] for team in teams}


# Generate all possible final tables.
simulate_matches(0, starting_points, [])


# Print every final table.
print("\nALL POSSIBLE FINAL TABLES")
print("=" * 70)

for table_number, final_table in enumerate(all_final_tables, start=1):
    print(f"\nTable {table_number}:")
    print("Winner path:", " -> ".join(final_table["winner_path"]))
    print("-" * 32)
    print(f"{'Rank':<6}{'Team':<8}{'Points':<8}{'Status'}")

    for rank, (team, points) in enumerate(final_table["table"], start=1):
        status = "Top 4" if team in final_table["top_4"] else "Outside"
        print(f"{rank:<6}{team:<8}{points:<8}{status}")


# Print final playoff probabilities.
total_tables = len(all_final_tables)

print("\n\nPLAYOFF PROBABILITY")
print("=" * 70)
print(f"Total final tables checked: {total_tables}\n")
print(f"{'Team':<8}{'Qualifies In':<16}{'Probability'}")

for team in teams:
    team_name = team["team"]
    count = qualify_count[team_name]
    probability = round((count / total_tables) * 100)
    print(f"{team_name:<8}{str(count) + ' / ' + str(total_tables):<16}{probability}%")
