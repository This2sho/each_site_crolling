
with open("test.json", "w", encoding="utf-8") as make_file:
    json.dump(data, make_file, indent="\t", ensure_ascii=False)
