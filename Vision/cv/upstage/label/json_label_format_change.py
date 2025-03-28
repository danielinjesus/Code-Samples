import json

def convert_json(input_file, output_file):
  with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

  new_data = []
  for image in data['images']:
    annotations = [anno for anno in data['annotations'] if anno['image_id'] == image['id']]
    new_data.append({
      "data": {
        "image": "/data/upload/images/" + image['file_name'],
        "annotations": annotations,
        "images": [image]
      }
    })

  with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(new_data, f, indent=2, ensure_ascii=False)

# JSON 파일 경로
input_file = '간판_세로형간판_000002.json'
output_file = 'converted.json'

convert_json(input_file, output_file)