from src.function import extract_compressor_data,plot_compressor_graph, goto_root

json_file = "datas/json_files/yak-3.json"

goto_root()
compressor_data = extract_compressor_data(json_file)
plot_compressor_graph(compressor_data)