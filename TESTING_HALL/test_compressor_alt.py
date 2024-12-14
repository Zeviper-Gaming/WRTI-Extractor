from src.function import analyze_compressor_power, goto_root

json_file = "datas/json_files/yak-3.json"

goto_root()
output = analyze_compressor_power(json_file)