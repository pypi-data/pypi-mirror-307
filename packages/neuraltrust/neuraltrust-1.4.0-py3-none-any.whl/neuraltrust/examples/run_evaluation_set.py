from neuraltrust import NeuralTrust

client = NeuralTrust(
    api_key="37d75589-7519-4e39-aa57-7120829e5aef:c147141e49fb37ce5ff8be7cbdeb6c84b057dc3005ebccede6a26ea8b71152e1"
)

client.run_evaluation_set(id="eval_set_12345")