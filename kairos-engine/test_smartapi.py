from SmartApi import SmartConnect
import pyotp
import traceback

def test_login():
    try:
        api_key = "dmsnd4rJ"
        client_code = "N51690180"
        pin = "1973"
        totp_key = "N2NZJ64ZWR2TY2PSNUSLZAKK2A"

        print("Initializing SmartConnect...")
        obj = SmartConnect(api_key=api_key)
        
        print("Generating TOTP...")
        totp = pyotp.TOTP(totp_key).now()
        print(f"Generated TOTP: {totp}")
        
        print("Attempting login...")
        data = obj.generateSession(client_code, pin, totp)
        
        if data.get('status') == False:
            print("Login failed!")
            print(data)
        else:
            print("Login successful!")
            print("Response Data:", data)
            
            # Fetch profile
            try:
                profile = obj.getProfile(data['data']['refreshToken'])
                print("Profile fetched successfully!")
                print("Name:", profile['data']['name'])
                print("Exchanges:", profile['data']['exchanges'])
            except Exception as e:
                print(f"Error fetching profile: {e}")

    except Exception as e:
        print(f"Error occurred: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    test_login()
