from opensearchpy import OpenSearch, RequestError

host = "localhost"
port = 9200
auth = ("admin", "admin")
ca_certs_path = "root-ca.pem"

client = OpenSearch(
    hosts=[{"host": host, "port": port}],
    http_compress=True,
    http_auth=auth,
    use_ssl=True,
    verify_certs=True,
    ssl_assert_hostname=False,
    ssl_show_warn=False,
    ca_certs=ca_certs_path,
)


index_name = "python-test-index"


def create_index() -> None:
    index_body = {
        "settings": {
            "index": {
                "number_of_shards": 4,
            }
        }
    }

    try:
        res = client.indices.create(index=index_name, body=index_body)
        print(res)
    except RequestError as e:
        print("skip", e)


def index_doc() -> None:
    doc = {
        "title": "Moneyball",
        "director": "Bennett Miller",
        "year": "2011",
    }

    res = client.index(index=index_name, body=doc, id="1", refresh=True)
    print(res)


def bulk_doc() -> None:
    movies = '{ "index" : { "_index" : "python-test-index", "_id" : "2" } } \n { "title" : "Interstellar", "director" : "Christopher Nolan", "year" : "2014"} \n { "create" : { "_index" : "python-test-index", "_id" : "3" } } \n { "title" : "Star Trek Beyond", "director" : "Justin Lin", "year" : "2015"} \n { "update" : {"_id" : "3", "_index" : "python-test-index" } } \n { "doc" : {"year" : "2016"} }'
    client.bulk(body=movies)


def search_doc() -> None:
    q = "miller"
    query = {
        "size": 5,
        "query": {
            "multi_match": {
                "query": q,
                "fields": ["title^2", "director"],
            },
        },
    }

    res = client.search(body=query, index=index_name)
    print(res)


def delete_doc() -> None:
    res = client.delete(index=index_name, id="1")
    print(res)


def delete_index() -> None:
    res = client.indices.delete(index=index_name)
    print(res)


def search_ghibli_movies() -> None:
    index_name = "movies"
    q = "Hayao Miyazaki"
    query = {
        "size": 5,
        "query": {
            "multi_match": {
                "query": q,
                "fields": ["directors"],
            },
        },
    }
    res = client.search(body=query, index=index_name)
    for hit in res["hits"]["hits"]:
        print(hit["_source"]["title"])


def main() -> None:
    # create_index()
    # index_doc()
    # bulk_doc()
    # search_doc()
    # delete_doc()
    # delete_index()
    search_ghibli_movies()


if __name__ == "__main__":
    main()
