from neuraltrust import NeuralTrust

client = NeuralTrust(
    api_key="37d75589-7519-4e39-aa57-7120829e5aef:c147141e49fb37ce5ff8be7cbdeb6c84b057dc3005ebccede6a26ea8b71152e1"
)

topics = [
    "Comidas y menús a bordo",
]


for topic in topics:
    try:
        knowledge_base = client.create_knowledge_base(
            type="upstash", 
            credentials={
                'UPSTASH_URL': "https://known-ocelot-13566-eu1-vector.upstash.io", 
                "UPSTASH_TOKEN": "ABYFMGtub3duLW9jZWxvdC0xMzU2Ni1ldTFhZG1pbk9UZzBNVFZpWXpndFpHWmxaaTAwTURNeExUa3dabVF0TnpFek56ZGlaV0k0TTJWaQ=="
            },
            seed_topics=[topic]
        )

        eval_functional = client.create_evaluation_set(
            name='Adversarial: ' + topic, 
            description='Eres un agente de AirTrust encargado de responder preguntas a los clientes de AirTrust.'
        )

        print("Generating adversarial testset for " + topic)
        # Type could be "functional", "adversarial" or "compliance"
        adversarial_testset = client.create_testset(
            name=topic,
            type="adversarial",
            evaluation_set_id=eval_functional.id,
            num_questions=8,
            knowledge_base_id=knowledge_base.id
        )

        client.run_evaluation_set(id=eval_functional.id)

        print(f"Successfully processed {topic}")
    except Exception as e:
        import traceback
        traceback.print_exc()

print("All topics have been processed.")


