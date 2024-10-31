import requests
import time

# Set up constants for the API
API_URL = "http://localhost:50325/api/v1"
API_KEY = "YOUR_API_KEY"  # Replace with your actual API key
HEADERS = {
    "Authorization": f"Bearer {API_KEY}"
}

def get_all_groups():
    """Fetches all groups from AdsPower."""
    response = requests.get(f"{API_URL}/groups", headers=HEADERS)
    if response.status_code == 200:
        groups = response.json()
        print("Groups retrieved successfully:")
        for group in groups:
            print(f"Group ID: {group['id']}, Name: {group['name']}")
        return groups
    else:
        print(f"Failed to retrieve groups: {response.status_code}")
        return None

def move_profile(profile_id, target_group_id):
    """Moves a single profile to the specified group."""
    data = {
        "profile_id": profile_id,
        "target_group_id": target_group_id
    }
    response = requests.post(f"{API_URL}/profiles/move", json=data, headers=HEADERS)
    if response.status_code == 200:
        print(f"Profile {profile_id} moved to group {target_group_id} successfully.")
    else:
        print(f"Failed to move profile {profile_id}: {response.status_code}, {response.text}")

def batch_move_profiles(profiles_to_move):
    """Moves multiple profiles to their respective target groups."""
    for profile in profiles_to_move:
        move_profile(profile["profile_id"], profile["target_group_id"])
        time.sleep(1)  # Respect API rate limit of 1 request per second

# Main execution
if __name__ == "__main__":
    # Step 1: Get all groups
    groups = get_all_groups()
    if not groups:
        print("Exiting due to inability to retrieve groups.")
    else:
        # Step 2: Define the profiles to move
        profiles_to_move = [
            {"profile_id": "PROFILE_ID_1", "target_group_id": "TARGET_GROUP_ID_1"},
            {"profile_id": "PROFILE_ID_2", "target_group_id": "TARGET_GROUP_ID_2"},
            # Add more profiles and target groups as needed
        ]
        
        # Step 3: Execute batch move
        print("Starting batch profile transfer...")
        batch_move_profiles(profiles_to_move)
        print("Batch transfer complete.")
