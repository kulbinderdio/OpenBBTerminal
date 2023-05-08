import pytest
import requests

# IMPORTATION INTERNAL
from openbb_terminal.alternative.companieshouse import companieshouse_model
from openbb_terminal.alternative.companieshouse.company_doc import CompanyDocument


def test_get_search_results(mocker):
    mock_response = mocker.Mock()
    mock_response.json.return_value = {
        "total_results": 2369,
        "items": [
            {
                "kind": "searchresults#company",
                "matches": {"title": [1, 5], "snippet": [13, 17]},
                "links": {"self": "/company/04366849"},
                "company_type": "plc",
                "address": {
                    "premises": "Shell Centre",
                    "address_line_1": "London",
                    "postal_code": "SE1 7NA",
                },
                "description": "04366849 - Incorporated on  5 February 2002",
                "snippet": "ROYAL DUTCH SHELL ",
                "title": "SHELL PLC",
                "company_status": "active",
                "date_of_creation": "2002-02-05",
                "address_snippet": "Shell Centre, London, SE1 7NA",
                "description_identifier": ["incorporated-on"],
                "company_number": "04366849",
            },
            {
                "address_snippet": "Shell Centre, York Road, London, United Kingdom, SE1 7NA",
                "description_identifier": ["incorporated-on"],
                "company_number": "03323845",
                "date_of_creation": "1997-02-25",
                "links": {"self": "/company/03323845"},
                "matches": {"title": [1, 5], "snippet": [1, 5]},
                "company_type": "ltd",
                "address": {
                    "address_line_1": "York Road",
                    "postal_code": "SE1 7NA",
                    "country": "United Kingdom",
                    "premises": "Shell Centre",
                    "locality": "London",
                },
                "kind": "searchresults#company",
                "snippet": "SHELL ",
                "title": "SHELL GROUP LIMITED",
                "company_status": "active",
                "description": "03323845 - Incorporated on 25 February 1997",
            },
        ],
        "items_per_page": 2,
        "kind": "search#companies",
        "start_index": 0,
        "page_number": 1,
    }

    mocker.patch.object(requests, "get", return_value=mock_response)

    # Call the function that makes a request to the remote API
    result = companieshouse_model.get_search_results("shell", 2)

    assert len(result) == 2
    assert result["Name"].iloc[0] == "SHELL PLC"
    assert result["Company Number"].iloc[0] == "04366849"


def test_get_persons_with_significant_control(mocker):
    mock_response = mocker.Mock()
    mock_response.json.return_value = {
        "ceased_count": 0,
        "items_per_page": 25,
        "total_results": 1,
        "active_count": 1,
        "start_index": 0,
        "items": [
            {
                "notified_on": "2020-12-18",
                "links": {
                    "self": "/company/13090621/persons-with-significant-control/individual/vLLtcUU1xdVC4x3tXu2szkiDluE"
                },
                "etag": "69ad137b49c648c6dd013761b82b52e6a7d474cb",
                "kind": "individual-person-with-significant-control",
                "country_of_residence": "England",
                "name": "Mrs Shelley Ann Fray",
                "natures_of_control": [
                    "ownership-of-shares-75-to-100-percent",
                    "voting-rights-75-to-100-percent",
                    "right-to-appoint-and-remove-directors",
                ],
                "nationality": "British",
                "address": {
                    "address_line_1": "Broadway",
                    "premises": "476-478",
                    "address_line_2": "Chadderton",
                    "country": "England",
                    "locality": "Oldham",
                    "postal_code": "OL9 9NS",
                },
                "date_of_birth": {"month": 6, "year": 1985},
                "name_elements": {
                    "surname": "Fray",
                    "middle_name": "Ann",
                    "title": "Mrs",
                    "forename": "Shelley",
                },
            }
        ],
        "links": {"self": "/company/13090621/persons-with-significant-control"},
    }

    mocker.patch.object(requests, "get", return_value=mock_response)

    # Call the function that makes a request to the remote API
    result = companieshouse_model.get_persons_with_significant_control("13090621")

    assert result["Name"].iloc[0] == "Mrs Shelley Ann Fray"


def test_get_officers(mocker):
    mock_response = mocker.Mock()
    mock_response.json.return_value = {
        "total_results": 1,
        "links": {"self": "/company/13090621/officers"},
        "items_per_page": 35,
        "items": [
            {
                "links": {
                    "self": "/company/13090621/appointments/y2Xs68vEDqfz-zbmxzc4QucY8fQ",
                    "officer": {
                        "appointments": "/officers/MSVxvbR-XzoxCZazKccwdkkmCYE/appointments"
                    },
                },
                "date_of_birth": {"month": 6, "year": 1985},
                "address": {
                    "country": "England",
                    "address_line_2": "Chadderton",
                    "address_line_1": "Broadway",
                    "locality": "Oldham",
                    "premises": "476-478",
                    "postal_code": "OL9 9NS",
                },
                "name": "FRAY, Shelley Ann",
                "occupation": "Director",
                "appointed_on": "2020-12-18",
                "country_of_residence": "England",
                "officer_role": "director",
                "nationality": "British",
            }
        ],
        "etag": "1138d965d225f6a0e5685c6d35e84e6a2dc0fc4f",
        "resigned_count": 0,
        "start_index": 0,
        "inactive_count": 0,
        "active_count": 1,
        "kind": "officer-list",
    }

    mocker.patch.object(requests, "get", return_value=mock_response)

    # Call the function that makes a request to the remote API
    result = companieshouse_model.get_officers("13090621")

    assert len(result) == 1
    assert result["Officer Role"].iloc[0] == "director"


def test_get_filings(mocker):
    mock_response = mocker.Mock()
    mock_response.json.return_value = {
        "total_count": 3,
        "items_per_page": 25,
        "items": [
            {
                "action_date": "2022-12-17",
                "category": "confirmation-statement",
                "date": "2023-01-06",
                "description": "confirmation-statement-with-no-updates",
                "description_values": {"made_up_date": "2022-12-17"},
                "links": {
                    "self": "/company/13090621/filing-history/MzM2NDcxNTAzMWFkaXF6a2N4",
                    "document_metadata": "https://frontend-doc-api.company-information.service.gov.uk/document/ZIvXc9ye1Y9q7FaE5mPNlwe1XghXICPgIhdoXoKxgjE",
                },
                "type": "CS01",
                "pages": 3,
                "barcode": "XBUK9D4X",
                "transaction_id": "MzM2NDcxNTAzMWFkaXF6a2N4",
            },
            {
                "category": "accounts",
                "date": "2022-09-14",
                "description": "accounts-with-accounts-type-unaudited-abridged",
                "description_values": {"made_up_date": "2021-12-31"},
                "links": {
                    "self": "/company/13090621/filing-history/MzM1MTY4NjU5NmFkaXF6a2N4",
                    "document_metadata": "https://frontend-doc-api.company-information.service.gov.uk/document/8_jguL3wGhY4CYashWk47Z5Zd-h5QpW4bQKT15Qgorc",
                },
                "type": "AA",
                "pages": 9,
                "barcode": "XBCG6V3N",
                "transaction_id": "MzM1MTY4NjU5NmFkaXF6a2N4",
            },
            {
                "action_date": "2022-09-09",
                "category": "address",
                "date": "2022-09-09",
                "description": "change-registered-office-address-company-with-date-old-address-new-address",
                "description_values": {
                    "change_date": "2022-09-09",
                    "old_address": "1J Shillington Old School Este Road London SW11 2TB",
                    "new_address": "476-478 Broadway Chadderton Oldham OL9 9NS",
                },
                "links": {
                    "self": "/company/13090621/filing-history/MzM1MTIwMjE4NGFkaXF6a2N4",
                    "document_metadata": "https://frontend-doc-api.company-information.service.gov.uk/document/h1b5B84vYbJ2dqXuxSALZNdNV3J9pv_RmxUSVGj2Yes",
                },
                "type": "AD01",
                "pages": 1,
                "barcode": "XBC30YEG",
                "transaction_id": "MzM1MTIwMjE4NGFkaXF6a2N4",
            },
        ],
        "start_index": 0,
        "filing_history_status": "filing-history-available",
    }

    mocker.patch.object(requests, "get", return_value=mock_response)

    # Call the function that makes a request to the remote API
    result = companieshouse_model.get_filings("13090621")

    assert len(result) == 3
    assert result["Category"].iloc[0] == "confirmation-statement"


def test_get_filing_document(mocker):
    result = CompanyDocument(
        "confirmation-statement",
        "2023-01-06",
        "confirmation-statement-with-no-updates",
        "paper_filed",
        3,
        "MzM2NDcxNTAzMWFkaXF6a2N4",
        "content",
    )

    assert result.description == "confirmation-statement-with-no-updates"
    assert result.pages == 3
