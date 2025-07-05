from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL

# Get default audio device using Pycaw
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# Get current volume (float value between -65.25 and 0.0 dB)
current_db = volume.GetMasterVolumeLevel()
current_vol_scalar = volume.GetMasterVolumeLevelScalar()  # 0.0 to 1.0

print(f"Current Volume: {int(current_vol_scalar * 100)}%")

while True:
    user_input = input("Type 'quit' to exit or enter volume (0-100): ")

    if user_input.lower() == 'quit':
        break

    if user_input.isdigit():
        vol = int(user_input)
        if 0 <= vol <= 100:
            volume.SetMasterVolumeLevelScalar(vol / 100, None)
            print(f"Volume set to {vol}%")
        else:
            print("Volume must be between 0 and 100.")
    else:
        print("Invalid input.")
