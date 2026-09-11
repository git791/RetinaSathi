import requests

API_URL = 'http://localhost:8001/api/v1/screenings'

def test_image(img_path, name):
    print(f"\n--- Testing {name} ---")
    try:
        with open(img_path, 'rb') as f:
            files = {'image': (img_path, f, 'image/png')}
            resp = requests.post(API_URL, files=files)
            print(f"Status Code: {resp.status_code}")
            data = resp.json()
            print("KEYS:", data.keys())
            
            print(f"Quality: {data.get('qualityStatus')}")
            
            ai_result = data.get('aiResult')
            if ai_result:
                print(f"Predicted Level: {ai_result.get('predictedLevel')}")
                print(f"Referable: {ai_result.get('referable')}")
            else:
                print("aiResult is null")
                
            explainability = data.get('explainability')
            if explainability and explainability.get('gradCAMUrl'):
                print("Grad-CAM available: TRUE")
            else:
                print("Grad-CAM available: FALSE")
                
            if data.get('qualityMessage'):
                print(f"Message: {data.get('qualityMessage')}")
    except Exception as e:
        print(f"Error: {e}")

aptos_path = 'C:\\Users\\moham\\OneDrive\\Desktop\\Documents\\MATLAB\\data\\APTOS\\train_images\\000c1434d8d7.png'
test_image(aptos_path, 'Real APTOS Image')

black_path = 'black.png'
test_image(black_path, 'Black/Ungradable Image')
