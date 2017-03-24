# Test steps for checking ElasticSearch indices
import datetime
import time
from behave import then

@then("the {es_index_prefix} template should have been uploaded")
def check_es_index_template(context, es_index_prefix):
    template_name = es_index_prefix + "-template"
    es_indices = context.es_client.indices
    retry_count = 40
    retry_interval = 1
    has_template = es_indices.exists_template(name=template_name)
    while not has_template and retry_count:
        # Give the indexer some time to start and upload the template
        retry_count -= 1
        time.sleep(retry_interval)
        has_template = es_indices.exists_template(name=template_name)
    assert has_template

@then("I should see {kind} {es_index_prefix} entries for {ecosystem}/{package}/{version}")
def check_analysis_history(context, kind, es_index_prefix, ecosystem, package, version):
    if kind != "component":
        raise ValueError("Tests currently only check component analysis history")
    index_shard_format = es_index_prefix + "-{:%Y.%m.%d}"
    finish_time = datetime.datetime.utcnow() # datetime.datetime.strptime(res["finished_at"], "%Y-%m-%dT%H:%M:%S.%f")
    index_shard = index_shard_format.format(finish_time)
    print(index_shard)
    es_client = context.es_client
    es_query = {"query": {"match_all": {}}}
    expected_types = context.get_expected_component_analyses(ecosystem)

    def _query_analysis_history():
        search_result = es_client.search(index=index_shard, body=es_query, size=len(expected_types) + 10)
        records = (hit["_source"] for hit in search_result["hits"]["hits"])
        analysis_types = set(record.get("analysis_type") for record in records)
        return context.compare_analysis_sets(analysis_types, expected_types)

    missing, unexpected = _query_analysis_history()
    retry_count = 3
    retry_interval = 30
    while retry_count and missing:
        # Give the indexer another chance to run
        retry_count -= 1
        time.sleep(retry_interval)
        missing, unexpected = _query_analysis_history()

    err_str = 'unexpected analyses: {}, missing analyses: {}'
    assert not missing and not unexpected, err_str.format(unexpected, missing)
