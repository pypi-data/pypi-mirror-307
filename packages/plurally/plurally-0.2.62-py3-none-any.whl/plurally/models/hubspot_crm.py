import enum
import os
import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any, List, Union

import tenacity
from hubspot import HubSpot
from hubspot.crm.companies.models import (
    PublicAssociationsForObject as CompanyPublicAssociationsForObject,
)
from hubspot.crm.companies.models import (
    PublicObjectSearchRequest as CompanyPublicObjectSearchRequest,
)
from hubspot.crm.companies.models import (
    SimplePublicObjectInputForCreate as CompanySimplePublicObjectInputForCreate,
)
from hubspot.crm.contacts import (
    PublicAssociationsForObject as ContactPublicAssociationsForObject,
)
from hubspot.crm.contacts import (
    PublicObjectSearchRequest as ContactPublicObjectSearchRequest,
)
from hubspot.crm.contacts import (
    SimplePublicObjectInputForCreate as ContactSimplePublicObjectInputForCreate,
)
from hubspot.crm.deals.models import (
    PublicAssociationsForObject as DealPublicAssociationsForObject,
)
from hubspot.crm.deals.models import (
    PublicObjectSearchRequest as DealPublicObjectSearchRequest,
)
from hubspot.crm.deals.models import (
    SimplePublicObjectInputForCreate as DealSimplePublicObjectInputForCreate,
)
from hubspot.crm.objects import (
    AssociationSpec,
    PublicAssociationsForObject,
    PublicObjectSearchRequest,
    SimplePublicObjectInput,
)
from loguru import logger
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    create_model,
    field_validator,
    model_validator,
)

from plurally.json_utils import replace_refs
from plurally.models import hubspot_industries, utils
from plurally.models.misc import Table
from plurally.models.node import Node

HUBSPOT_FILTERS_TYPE_FRIENDLY = "Hubspot Filters"
DEFAULT_CONTACT_PROPERTIES = "email, firstname, lastname, phone, company, jobtitle"
DEFAULT_COMPANY_PROPERTIES = "domain, name, industry, description"
DEFAULT_DEAL_PROPERTIES = "dealname, amount, dealstage, closedate"
DEFAULT_CALL_PROPERTIES = "hs_timestamp, hs_call_title, hs_call_body"
REQUIRED_CONTACT_PROPERTIES = ("email",)
REQUIRED_COMPANY_PROPERTIES = ("domain",)
REQUIRED_DEAL_PROPERTIES = ("dealname",)
REQUIRED_CALL_PROPERTIES = ("hs_call_title", "hs_timestamp")


class HubspotDealStage(Enum):
    APPOINTMENT_SCHEDULED = "appointmentscheduled"
    QUALIFIED_TO_BUY = "qualifiedtobuy"
    PRESENTATION_SCHEDULED = "presentationscheduled"
    DECISION_MAKER_BOUGHT_IN = "decisionmakerboughtin"
    CONTRACT_SENT = "contractsent"
    CLOSED_WON = "closedwon"
    CLOSED_LOST = "closedlost"


class HubspotModelBase(BaseModel):
    model_config = ConfigDict(use_enum_values=True)


class HubspotCallCreateModel(HubspotModelBase): ...


class HubspotCallReadModel(HubspotModelBase):
    id: str


class HubspotCompanyCreateModel(HubspotModelBase): ...


class HubspotCompanyReadModel(HubspotModelBase):
    id: str


class HubspotContactCreateModel(HubspotModelBase): ...


class HubspotContactReadModel(HubspotModelBase):
    id: str


class HubspotDealCreateModel(HubspotModelBase): ...


class HubspotDealReadModel(HubspotModelBase):
    id: str


BASE_CLASSES = {
    "HubspotCallCreate": HubspotCallCreateModel,
    "HubspotCallRead": HubspotCallReadModel,
    "HubspotCompanyCreate": HubspotCompanyCreateModel,
    "HubspotCompanyRead": HubspotCompanyReadModel,
    "HubspotContactCreate": HubspotContactCreateModel,
    "HubspotContactRead": HubspotContactReadModel,
    "HubspotDealCreate": HubspotDealCreateModel,
    "HubspotDealRead": HubspotDealReadModel,
}


class HubspotObjectType(Enum):
    CALL = "call"
    CONTACT = "contact"
    COMPANY = "company"
    DEAL = "deal"


SEARCH_API_CLASSES = {
    HubspotObjectType.COMPANY: CompanyPublicObjectSearchRequest,
    HubspotObjectType.CONTACT: ContactPublicObjectSearchRequest,
    HubspotObjectType.DEAL: DealPublicObjectSearchRequest,
}

API_NAMES = {
    HubspotObjectType.COMPANY: "companies",
    HubspotObjectType.CONTACT: "contacts",
    HubspotObjectType.DEAL: "deals",
}


class HubspotOperator(enum.Enum):
    LT = "LT"
    LTE = "LTE"
    GT = "GT"
    GTE = "GTE"
    EQ = "EQ"
    NEQ = "NEQ"
    BETWEEN = "BETWEEN"
    IN = "IN"
    NOT_IN = "NOT_IN"
    HAS_PROPERTY = "HAS_PROPERTY"
    NOT_HAS_PROPERTY = "NOT_HAS_PROPERTY"
    CONTAINS_TOKEN = "CONTAINS_TOKEN"
    NOT_CONTAINS_TOKEN = "NOT_CONTAINS_TOKEN"


class HubspotFilter(BaseModel):
    model_config = ConfigDict(use_enum_values=True)
    propertyName: str
    operator: HubspotOperator
    value: Any


class HubspotFilterDict(BaseModel):
    filters: List[HubspotFilter]


class HubspotBase(Node):
    SCOPES = [
        "crm.objects.contacts.read",
        "crm.objects.contacts.write",
        "crm.objects.companies.read",
        "crm.objects.companies.write",
        "crm.objects.deals.read",
        "crm.objects.deals.write",
    ]
    ICON = "hubspot"

    def __init__(self, init_inputs: Node.InitSchema):
        super().__init__(init_inputs)
        assert self.SCOPES is not None, "SCOPES must be defined in the subclass"
        self._service = None
        self._token = None
        self._token_expiry = None

    def token(self):
        now = datetime.now(tz=timezone.utc).replace(tzinfo=None)
        if self._token is None or self._token_expiry < now:
            self.reset()
            self._token, self._token_expiry = utils.get_access_token(self.SCOPES)
        return self._token

    @property
    def service(self) -> HubSpot:
        if self._service is None:
            self._service = HubSpot(access_token=self.token())
        return self._service

    def reset(self):
        self._token = None
        self._token_expiry = None
        self._service = None


class ContactAssociationProperties(Enum):
    EMAIL = "email"
    LASTNAME = "last name"
    FIRSTNAME = "first name"


class CompanyAssociationProperties(Enum):
    DOMAIN = "domain"
    NAME = "name"


class DealAssociationProperties(Enum):
    DEALNAME = "dealname"


class CallAssociationProperties(Enum):
    HS_CALL_TITLE = "hs_call_title"


PROPERTIES = {
    HubspotObjectType.CONTACT: ContactAssociationProperties,
    HubspotObjectType.COMPANY: CompanyAssociationProperties,
    HubspotObjectType.DEAL: DealAssociationProperties,
    HubspotObjectType.CALL: CallAssociationProperties,
}


supported_operators = [
    HubspotOperator.EQ,
    HubspotOperator.NEQ,
    HubspotOperator.IN,
    HubspotOperator.NOT_IN,
    HubspotOperator.HAS_PROPERTY,
    HubspotOperator.NOT_HAS_PROPERTY,
    HubspotOperator.CONTAINS_TOKEN,
    HubspotOperator.NOT_CONTAINS_TOKEN,
]
_SupportedOperators = Enum(
    "SupportedOperators", [(v.name, v.value) for v in supported_operators]
)


def get_hubspot_association_filter_kls(object_type: HubspotObjectType):
    possible_to_object_types = [v for v in HubspotObjectType if v != object_type]
    _ToObjectType = Enum(
        "ToObjectType", [(v.name, v.value) for v in possible_to_object_types]
    )
    default_object_type = possible_to_object_types[0]
    to_object_type_one_of = []
    for to_object_type in possible_to_object_types:
        property_names = [p.value for p in PROPERTIES[to_object_type]]
        to_object_type_one_of.append(
            {
                "properties": {
                    "to_object_type": {"const": to_object_type.value},
                    f"{to_object_type.value}_property_name": {
                        "enum": property_names,
                        "title": "Property",
                        "description": "The property to use for the association.",
                        "default": property_names[0],
                    },
                },
                "required": ["to_object_type", f"{to_object_type.value}_property_name"],
            }
        )

    class HubspotAssociationFilter(BaseModel):
        to_object_type: _ToObjectType = Field(  # type: ignore
            default_object_type.value,
            title="Type",
            description="The type of the object to associate to.",
        )
        operator: _SupportedOperators = Field(  # type: ignore
            HubspotOperator.EQ,
            title="Operator",
            description="The operator to use for the association.",
        )
        model_config = ConfigDict(
            use_enum_values=True,
            json_schema_extra={
                "dependencies": {"to_object_type": {"oneOf": to_object_type_one_of}}
            },
        )

        # we do not want this in UI Form, it's handled with the dependencies
        # but we need it for programmatic instantiation
        # therefore we hide it (computed field won't cut it)
        property_name: str | None = Field(None, format="hidden")

        @field_validator("to_object_type", mode="after")
        def validate_to_object_type(cls, v):
            return HubspotObjectType(v if isinstance(v, str) else v.name).value

        @field_validator("operator", mode="after")
        def validate_operator(cls, v):
            return HubspotOperator(v if isinstance(v, str) else v.name).value

        @model_validator(mode="before")
        @classmethod
        def validate_model(cls, data):
            for obj_type in possible_to_object_types:
                selected_obj_type = HubspotObjectType(data["to_object_type"])
                if obj_type == selected_obj_type:
                    allowed_props = [p.value for p in PROPERTIES[obj_type]]
                    # we must override here - as if the user selects a different to_object_type
                    # the property_name will be set to an invalid value
                    key = f"{obj_type.value}_property_name"
                    if key in data:
                        # override
                        data["property_name"] = data[key]
                    # we keep property_name only if not specific key is present
                    # as this means that it was parsed from serialization (specific keys are not serialized)
                    if "property_name" not in data:
                        raise ValueError(
                            f"Could not find generic or specific key for property_name in {data}"
                        )
                    if data["property_name"] not in allowed_props:
                        raise ValueError(
                            f"Property name must be one of {allowed_props}"
                        )
                    break
            else:
                raise ValueError(f"Invalid to_object_type {data['to_object_type']}")
            return data

    return HubspotAssociationFilter


HubspotCompanyAssociationFilter = get_hubspot_association_filter_kls(
    HubspotObjectType.COMPANY
)
HubspotContactAssociationFilter = get_hubspot_association_filter_kls(
    HubspotObjectType.CONTACT
)
HubspotDealAssociationFilter = get_hubspot_association_filter_kls(
    HubspotObjectType.DEAL
)

ASSOCS_FILTERS = {
    HubspotObjectType.COMPANY: HubspotCompanyAssociationFilter,
    HubspotObjectType.CONTACT: HubspotContactAssociationFilter,
    HubspotObjectType.DEAL: HubspotDealAssociationFilter,
}


class HubspotEntityReadBuilder:
    @classmethod
    def build(
        cls,
        object_type: HubspotObjectType,
        properties_default: str,
        api_name: str,
    ):
        assoc_filter_type = get_hubspot_association_filter_kls(object_type)

        class HubspotEntityRead(HubspotBase):
            class InitSchema(Node.InitSchema):
                __doc__ = f"""Read {object_type.value.title()} from HubSpot. Possibility to filter by properties and associations."""

                properties: str = Field(
                    properties_default,
                    title="Properties",
                    description="The properties to fetch (comma separated).",
                    json_schema_extra={
                        "uiSchema": {
                            "ui:widget": "textarea",
                            "ui:placeholder": f"Comma separated properties, for example: {properties_default}",
                        }
                    },
                )
                associations: List[assoc_filter_type] = Field(  # type: ignore
                    [],
                    json_schema_extra={
                        "name_singular": "Association",
                        "uiSchema": {
                            "ui:label": False,
                            "items": {
                                "ui:label": False,
                                "ui:grid": [
                                    (
                                        "to_object_type",
                                        {
                                            "base": 12,
                                            "sm": 4,
                                        },
                                    ),
                                    *[
                                        (
                                            f"{o.value}_property_name",
                                            {"base": 12, "sm": 4},
                                        )
                                        for o in HubspotObjectType
                                        if o != object_type
                                    ],
                                    ("operator", {"base": 12, "sm": 4}),
                                ],
                            },
                        },
                    },
                )
                limit: int = Field(
                    100,
                    title="Limit",
                    description=f"The number of {object_type.value} to fetch.",
                    json_schema_extra={"advanced": True},
                )

            class OutputSchema(Node.OutputSchema):
                entities: Table = Field(..., title=f"{object_type.value.capitalize()}s")

            class InputSchema(Node.InputSchema):
                filter_groups: List[HubspotFilterDict] = Field(
                    [],
                    title="Filters",
                    description="The filters to apply in the search.",
                    json_schema_extra={"type-friendly": HUBSPOT_FILTERS_TYPE_FRIENDLY},
                )

            def __init__(self, init_inputs: Node.InitSchema):
                self.limit = init_inputs.limit
                self.properties = init_inputs.properties
                self._associations = init_inputs.associations
                super().__init__(init_inputs)

            @property
            def associations(self):
                return self._associations

            @associations.setter
            def associations(self, value):
                value = [
                    v if isinstance(v, assoc_filter_type) else assoc_filter_type(**v)
                    for v in value
                ]
                self._associations = value
                self._set_schemas()
                self.tgt_handles = self._get_handles(self.InputSchema, None)

            def _set_schemas(self):
                extra_inputs = {}
                for assoc in self.associations:
                    op = HubspotOperator(assoc.operator)
                    key = f"{assoc.to_object_type}_{assoc.property_name}"
                    desc = f"Association filter for {assoc.to_object_type.capitalize()} {assoc.property_name}."
                    if op in [
                        HubspotOperator.EQ,
                        HubspotOperator.NEQ,
                        HubspotOperator.CONTAINS_TOKEN,
                        HubspotOperator.NOT_CONTAINS_TOKEN,
                    ]:
                        title = (
                            f"{assoc.to_object_type.capitalize()} {assoc.property_name}"
                        )
                        extra_inputs[key] = (
                            str,  # ??? could be something else as well i guess
                            Field(
                                title=title,
                                description=desc,
                            ),
                        )
                    elif op in [HubspotOperator.IN, HubspotOperator.NOT_IN]:
                        title = (
                            f"{assoc.to_object_type.capitalize()} {assoc.property_name}"
                        )
                        extra_inputs[key] = (
                            List[str],
                            Field(
                                title=title,
                                description=desc,
                            ),
                        )
                    elif op in [
                        HubspotOperator.HAS_PROPERTY,
                        HubspotOperator.NOT_HAS_PROPERTY,
                    ]:
                        pass

                self.InputSchema = create_model(
                    f"{object_type.name.capitalize()}Input",
                    **extra_inputs,
                    __base__=HubspotEntityRead.InputSchema,
                )

            def serialize(self):
                return super().serialize() | {
                    "limit": self.limit,
                    "properties": self.properties,
                    "associations": [assoc.model_dump() for assoc in self.associations],
                    "input_schema": replace_refs(self.InputSchema.model_json_schema()),
                }

            def _build_query_for_assoc(self, assoc_filter: HubspotDealAssociationFilter, prop_val):  # type: ignore
                kls = SEARCH_API_CLASSES[HubspotObjectType(assoc_filter.to_object_type)]
                value_key = (
                    "values" if assoc_filter.operator in ["IN", "NOT_IN"] else "value"
                )
                return kls(
                    filter_groups=[
                        {
                            "filters": [
                                {
                                    "propertyName": assoc_filter.property_name,
                                    "operator": assoc_filter.operator,
                                    value_key: prop_val,
                                }
                            ]
                        }
                    ],
                    limit=100,
                )

            def _search_for_association(self, assoc_filter: HubspotDealAssociationFilter, prop_val):  # type: ignore
                if os.environ.get("VERBOSE"):
                    logger.debug(
                        f"Searching for object_type={assoc_filter=} {prop_val=}"
                    )
                api_name = API_NAMES[HubspotObjectType(assoc_filter.to_object_type)]
                return self.service.crm.objects.search_api.do_search(
                    object_type=api_name,
                    public_object_search_request=self._build_query_for_assoc(
                        assoc_filter, prop_val
                    ),
                ).results

            def _create_filter_from_assoc_filter(self, assoc_filter: HubspotDealAssociationFilter, prop_val):  # type: ignore
                search_res = self._search_for_association(assoc_filter, prop_val)
                if not search_res:
                    return None
                return {
                    "propertyName": f"associations.{assoc_filter.to_object_type}",
                    "operator": "IN",
                    "values": [entity.id for entity in search_res],
                }

            def _build_query(self, node_inputs) -> PublicObjectSearchRequest:
                filter_groups = node_inputs.model_dump()["filter_groups"]

                if self.associations:
                    assoc_filters = []
                    for assoc in self.associations:
                        key = f"{assoc.to_object_type}_{assoc.property_name}"
                        prop_val = getattr(node_inputs, key, None)

                        assoc_filter = self._create_filter_from_assoc_filter(
                            assoc, prop_val
                        )
                        if assoc_filter is None:
                            logger.debug(
                                f"No results when searching for object_type={assoc.to_object_type} "
                                f"with property_name={assoc.property_name} "
                                f"and op={assoc.operator}"
                            )
                            # this means that the user wants to filter by an association but there was no results.
                            # then this search should return no results
                            return None

                        logger.debug(f"Adding association filter: {assoc_filter}")
                        assoc_filters.append(assoc_filter)

                    filter_groups = filter_groups or [{"filters": []}]
                    for f in filter_groups:
                        f["filters"] = f.get("filters", []) + assoc_filters

                logger.debug(f"Filter groups: {filter_groups}")
                return PublicObjectSearchRequest(
                    properties=[s.strip() for s in self.properties.split(",")],
                    filter_groups=filter_groups,
                    limit=self.limit,
                )

            def forward(self, node_inputs: InputSchema):
                q = self._build_query(node_inputs)
                if q is None:
                    self.outputs = {"entities": Table(data=[])}
                    return

                entities = self.service.crm.objects.search_api.do_search(
                    object_type=api_name, public_object_search_request=q
                )
                self.outputs = {
                    "entities": Table(
                        data=[entity.properties for entity in entities.results]
                    )
                }

        return HubspotEntityRead


_HubspotCallsRead = HubspotEntityReadBuilder.build(
    HubspotObjectType.CALL,
    DEFAULT_CALL_PROPERTIES,
    "calls",
)


class HubspotCallsRead(_HubspotCallsRead):
    pass


_HubspotCompaniesRead = HubspotEntityReadBuilder.build(
    HubspotObjectType.COMPANY,
    DEFAULT_COMPANY_PROPERTIES,
    "companies",
)


class HubspotCompaniesRead(_HubspotCompaniesRead):
    pass


_HubspotContactsRead = HubspotEntityReadBuilder.build(
    HubspotObjectType.CONTACT,
    DEFAULT_CONTACT_PROPERTIES,
    "contacts",
)


class HubspotContactsRead(_HubspotContactsRead):
    pass


_HubspotDealsRead = HubspotEntityReadBuilder.build(
    HubspotObjectType.DEAL,
    DEFAULT_DEAL_PROPERTIES,
    "deals",
)


class HubspotDealsRead(_HubspotDealsRead):
    pass


def validate_properties_generic(v, req_props):
    v = [s.strip().lower() for s in v.split(",")]
    issues = []
    for req_prop in req_props:
        if req_prop not in v:
            issues.append(req_prop)
    if issues:
        raise ValueError(
            f"Properties must contain the following properties: {', '.join(issues)}"
        )
    return ",".join(v)


class HubspotEntityCreateBuilder:

    @classmethod
    def build(
        cls,
        entity_name: str,
        unique_property_name: str,
        properties_default: str,
        api_name: str,
        entity_create_kls,
        entity_associations_kls,
        entity_search_kls,
        extra_props: dict = None,
        get_validators=None,
        property_types=None,
        property_required=tuple(),
    ):
        class HubspotEntityCreate(HubspotBase):
            ENTITY_NAME_TITLE = entity_name.title()
            CREATE_BASE_KLS = BASE_CLASSES[f"Hubspot{ENTITY_NAME_TITLE}Create"]
            READ_BASE_KLS = BASE_CLASSES[f"Hubspot{ENTITY_NAME_TITLE}Read"]
            PROPERTY_TYPES = property_types or {}
            PROPERTY_REQUIRED = property_required

            class InitSchema(Node.InitSchema):
                __doc__ = f"""
Creates a HubSpot {entity_name.title()}.

This block requires you to connect your HubSpot account to Plurally.
                """
                properties: str = Field(
                    properties_default,
                    title="Properties",
                    description="The properties to assign (comma separated).",
                    json_schema_extra={
                        "uiSchema": {
                            "ui:widget": "textarea",
                            "ui:placeholder": f"Comma separated properties, for example: {properties_default}",
                        }
                    },
                )

                update_if_exists: bool = Field(
                    True,
                    title="Update if Exists",
                    description=f"If a {entity_name} with the same {unique_property_name} exists, update it.",
                    json_schema_extra={"advanced": True},
                )

                @field_validator("properties")
                def validate_properties(cls, v):
                    return validate_properties_generic(v, property_required)

            DESC = InitSchema.__doc__

            InputSchema = create_model(
                f"{ENTITY_NAME_TITLE}Input",
                **{
                    entity_name: (
                        CREATE_BASE_KLS,
                        Field(
                            ...,
                            title=f"Hubspot {ENTITY_NAME_TITLE}",
                            description=f"The {entity_name} to create or update.",
                            json_schema_extra={
                                "type-friendly": f"Hubspot {ENTITY_NAME_TITLE}",
                                "jit": True,
                            },
                        ),
                    ),
                    **(extra_props or {}),
                },
                __base__=Node.InputSchema,
            )

            OutputSchema = create_model(
                f"{ENTITY_NAME_TITLE}Input",
                **{
                    entity_name: (
                        READ_BASE_KLS,
                        Field(
                            ...,
                            title=f"Hubspot {ENTITY_NAME_TITLE}",
                            description=f"The {entity_name} that was created or updated.",
                            json_schema_extra={
                                "type-friendly": f"Hubspot {ENTITY_NAME_TITLE}",
                                "jit": True,
                            },
                        ),
                    )
                },
                __base__=Node.OutputSchema,
            )

            def __init__(self, init_inputs: Node.InitSchema):
                self._properties = init_inputs.properties
                self.update_if_exists = init_inputs.update_if_exists
                self.entity_name = entity_name
                super().__init__(init_inputs)

            @property
            def adapters(self):
                return super().adapters | {
                    entity_name: {
                        Association: get_entity_to_assoc(self.ENTITY_NAME_TITLE)
                    }
                }

            @property
            def properties(self):
                return self._properties

            @properties.setter
            def properties(self, value):
                self._properties = value
                self._set_schemas()

            @classmethod
            def get_property_type(cls, property_annot, is_required):
                if is_required:
                    return property_annot
                return Union[property_annot, None]

            @classmethod
            def get_entity_model(
                cls, properties, __base__, extra_props=None, __validators__=None
            ):
                entity = create_model(
                    f"Hubspot{cls.ENTITY_NAME_TITLE}",
                    **{
                        prop: (
                            cls.get_property_type(
                                cls.PROPERTY_TYPES.get(prop, str),
                                prop in cls.PROPERTY_REQUIRED,
                            ),
                            Field(
                                None,
                                title=prop,
                            ),
                        )
                        for prop in [s.strip() for s in properties.split(",")]
                    },
                    **(extra_props or {}),
                    __base__=__base__,
                    __validators__=__validators__,
                )
                return entity

            def _get_input_props(self):
                __validators__ = (
                    get_validators(self.properties) if get_validators else None
                )
                EntityModel = self.get_entity_model(
                    self.properties, self.CREATE_BASE_KLS, __validators__=__validators__
                )
                return {
                    entity_name: (
                        EntityModel,
                        Field(..., title=f"Hubspot {self.ENTITY_NAME_TITLE}"),
                    ),
                    **(extra_props or {}),
                }

            def _get_output_props(self):
                EntityModel = self.get_entity_model(self.properties, self.READ_BASE_KLS)
                return {
                    self.entity_name: (
                        EntityModel,
                        Field(..., title=f"Hubspot {self.ENTITY_NAME_TITLE}"),
                    )
                }

            def _set_schemas(self):
                self.InputSchema = create_model(
                    f"{self.ENTITY_NAME_TITLE}Input",
                    **self._get_input_props(),
                    __base__=Node.InputSchema,
                )
                self.OutputSchema = create_model(
                    f"{self.ENTITY_NAME_TITLE}Output",
                    **self._get_output_props(),
                    __base__=Node.OutputSchema,
                )

            def serialize(self):
                return super().serialize() | {
                    "properties": self._properties,
                    "update_if_exists": self.update_if_exists,
                }

            @property
            def basic_api(self):
                return self.basic_api_service(self.service)

            @classmethod
            def get_existing(cls, service, unique_property_value):
                q = entity_search_kls(
                    properties=[unique_property_name],
                    filter_groups=[
                        {
                            "filters": [
                                {
                                    "propertyName": unique_property_name,
                                    "operator": "EQ",
                                    "value": unique_property_value,
                                }
                            ]
                        }
                    ],
                    limit=1,
                )
                search_results = service.crm.objects.search_api.do_search(
                    object_type=api_name, public_object_search_request=q
                )
                if search_results.total > 0:
                    return search_results.results[0]

            @classmethod
            def create_entity(cls, service, create_data):
                entity = service.crm.objects.basic_api.create(
                    object_type=api_name,
                    simple_public_object_input_for_create=create_data,
                )
                logger.debug(f"Created {entity_name} with id={entity.id}")
                return entity

            @classmethod
            def create_or_update_entity(
                cls,
                service,
                input_entity,
                associations=None,
                update_if_exists=False,
            ):
                unique_property_value = getattr(input_entity, unique_property_name)
                if not unique_property_value:
                    logger.debug("No unique property value provided, early returning.")
                    return None
                is_update = False
                entity = cls.get_existing(service, unique_property_value)
                input_entity_data = input_entity.model_dump()
                if entity:
                    logger.debug(f"{entity_name} already exists.")
                    if update_if_exists is True:
                        logger.debug(f"Updating {entity_name} with id={entity.id}")
                        create_data = entity_create_kls(properties=input_entity_data)
                        entity = service.crm.objects.basic_api.update(
                            object_id=entity.id,
                            object_type=api_name,
                            simple_public_object_input=create_data,
                        )
                        is_update = True
                        if associations:
                            cls.associate(service, int(entity.id), associations)
                            entity = cls.get_existing(service, unique_property_value)
                    elif update_if_exists == "make_unique":
                        logger.debug(f"Making {entity_name} unique.")
                        # make unique property value unique
                        setattr(
                            input_entity,
                            unique_property_name,
                            f"{unique_property_value} {str(uuid.uuid4())[:4]}",
                        )
                        return cls.create_or_update_entity(
                            service,
                            input_entity,
                            associations,
                            update_if_exists,
                        )
                    else:
                        logger.debug("Skipping update.")
                else:
                    create_data = entity_create_kls(properties=input_entity_data)
                    entity = cls.create_entity(service, create_data)
                    if associations:
                        cls.associate(service, int(entity.id), associations)
                return entity, is_update

            @classmethod
            def create_or_update(
                cls,
                service,
                input_entity,
                associations,
                update_if_exists,
                output_schema_kls,
            ):
                entity, _ = cls.create_or_update_entity(
                    service,
                    input_entity,
                    associations,
                    update_if_exists,
                )
                return output_schema_kls(
                    **{entity_name: {**{"id": entity.id}, **entity.properties}}
                ).model_dump()

            @tenacity.retry(
                wait=tenacity.wait_fixed(5),
                stop=tenacity.stop_after_attempt(3),
            )
            def forward(self, node_inputs):
                entity = getattr(node_inputs, self.entity_name)
                self.outputs = self.create_or_update(
                    self.service,
                    entity,
                    node_inputs.associations,
                    self.update_if_exists,
                    self.OutputSchema,
                )

            @classmethod
            def associate(cls, service, entity_id, associations):
                # associations is a unique assoc for not
                # later might be a list, need to see
                # then the next line should be changed
                for association in [associations]:
                    # check if assoc exists
                    existing_assocs = service.crm.associations.v4.basic_api.get_page(
                        association.from_oject_type,
                        entity_id,
                        association.to_object_type,
                    )

                    if any(
                        existing_assoc.to_object_id == association.to.id
                        for existing_assoc in existing_assocs.results
                    ):
                        # assoc already exists, do nothing
                        logger.debug("Association already exists, skipping.")
                    else:
                        for existing_assoc in existing_assocs.results:
                            service.crm.associations.v4.basic_api.archive(
                                association.from_oject_type,
                                entity_id,
                                association.to_object_type,
                                existing_assoc.to_object_id,
                            )

                        args = [
                            association.from_oject_type,
                            entity_id,
                            association.to_object_type,
                            association.to.id,
                            [
                                AssociationSpec(
                                    association.types[0].associationCategory,
                                    association.types[0].associationTypeId,
                                )
                            ],
                        ]
                        logger.debug(f"Associating with {associations}")
                        return service.crm.associations.v4.basic_api.create(*args)

            def _get_cls_props(self):
                return {}

        return HubspotEntityCreate


class AssociationTo(BaseModel):
    id: str


class AssociationTypes(BaseModel):
    associationTypeId: int = Field()
    associationCategory: str = Field("HUBSPOT_DEFINED")


class Association(BaseModel):
    to: AssociationTo
    types: List[AssociationTypes]
    from_oject_type: str = Field(exclude=True)
    to_object_type: str = Field(exclude=True)


class ContactToCompany(Association):
    types: List[AssociationTypes] = [AssociationTypes(associationTypeId=279)]
    from_oject_type: str = "contact"
    to_object_type: str = "company"


class ContactToCall(Association):
    types: List[AssociationTypes] = [AssociationTypes(associationTypeId=193)]
    from_oject_type: str = "contact"
    to_object_type: str = "call"


class CallToContact(Association):
    types: List[AssociationTypes] = [AssociationTypes(associationTypeId=194)]
    from_oject_type: str = "call"
    to_object_type: str = "contact"


class DealToCompany(Association):
    types: List[AssociationTypes] = [AssociationTypes(associationTypeId=5)]
    from_oject_type: str = "deal"
    to_object_type: str = "company"


class HubspotContactToCompany(Node):

    ICON = "hubspot"

    class InitSchema(Node.InitSchema):
        """
        Create a HubSpot association between a contact and a company.
        """

    DESC = InitSchema.__doc__

    class InputSchema(Node.InputSchema):
        company: HubspotCompanyReadModel = None

    class OutputSchema(Node.OutputSchema):
        association: Association

    def forward(self, node_inputs: InputSchema):
        if not node_inputs.company:
            logger.debug("No company provided, skipping association creation.")
            return {}
        logger.debug(
            f"Creating association between contact and company with IDs: {node_inputs.company.id}"
        )
        self.outputs["association"] = ContactToCompany(
            to=AssociationTo(id=node_inputs.company.id),
        )


associations = {
    "associations": (Association, Field(None, title="Associations")),
}


_HubspotCallCreate = HubspotEntityCreateBuilder.build(
    "call",
    "hs_call_title",
    DEFAULT_CALL_PROPERTIES,
    "calls",
    SimplePublicObjectInput,
    PublicAssociationsForObject,
    PublicObjectSearchRequest,
    associations,
    property_types={"hs_timestamp": datetime},
    property_required=REQUIRED_CALL_PROPERTIES,
)


class HubspotCallCreate(_HubspotCallCreate):
    pass


_HubspotContactCreate = HubspotEntityCreateBuilder.build(
    "contact",
    "email",
    DEFAULT_CONTACT_PROPERTIES,
    "contacts",
    ContactSimplePublicObjectInputForCreate,
    ContactPublicAssociationsForObject,
    ContactPublicObjectSearchRequest,
    associations,
    property_required=REQUIRED_CONTACT_PROPERTIES,
)


class HubspotContactCreate(_HubspotContactCreate):
    pass


def validate_industry(v):
    v = hubspot_industries.to_enum_value_case(v)
    if v not in hubspot_industries.INDUSTRIES:
        return None
    return v


def get_company_validators(properties):
    validators = {}
    if "industry" in properties:
        # make sure it has a different name than the property
        validators["validate_industry"] = field_validator("industry")(validate_industry)
    return validators


_HubspotCompanyCreate = HubspotEntityCreateBuilder.build(
    "company",
    "domain",
    DEFAULT_COMPANY_PROPERTIES,
    "companies",
    CompanySimplePublicObjectInputForCreate,
    CompanyPublicAssociationsForObject,
    CompanyPublicObjectSearchRequest,
    associations,
    get_validators=get_company_validators,
    property_required=REQUIRED_COMPANY_PROPERTIES,
)


class HubspotCompanyCreate(_HubspotCompanyCreate):
    pass


_HubspotDealCreate = HubspotEntityCreateBuilder.build(
    "deal",
    "dealname",
    DEFAULT_DEAL_PROPERTIES,
    "deals",
    DealSimplePublicObjectInputForCreate,
    DealPublicAssociationsForObject,
    DealPublicObjectSearchRequest,
    associations,
    property_types={"dealstage": HubspotDealStage, "closedate": datetime},
    property_required=REQUIRED_DEAL_PROPERTIES,
)


class HubspotDealCreate(_HubspotDealCreate):
    pass


ASSOCS = {
    "HubspotContactToCompany": HubspotContactToCompany,
}


def get_entity_to_assoc(entity_name_title: str):
    def entity_to_assoc(src_node, tgt_node, src_handle):
        kls_name = f"Hubspot{tgt_node.ENTITY_NAME_TITLE}To{entity_name_title}"
        kls = ASSOCS.get(kls_name)
        if not kls:
            raise ValueError(f"Association {kls_name} not found.")
        nodes = [
            kls(
                kls.InitSchema(
                    name=f"Assoc. {tgt_node.ENTITY_NAME_TITLE} To {entity_name_title}",
                    pos_x=(src_node.pos_x + tgt_node.pos_x) / 2,
                    pos_y=(src_node.pos_y + tgt_node.pos_y) / 2,
                )
            )
        ]
        connections = [
            (0, src_handle, 1, src_node.entity_name),
            (1, "association", 2, None),
        ]
        return nodes, connections

    return entity_to_assoc


class HubspotContactToCompanyUnique(BaseModel):
    contact_email: str
    company_domain: str


class HubspotDealToCompanyUnique(BaseModel):
    dealname: str
    company_domain: str


class HubspotCallToContactUnique(BaseModel):
    hs_call_title: str
    contact_email: str


class HubSpotAutoEntity(HubspotModelBase):
    companies: List[HubspotCompanyCreateModel]
    contacts: List[HubspotContactCreateModel]
    deals: List[HubspotDealCreateModel]
    contact_to_company_assocs: List[HubspotContactToCompanyUnique]
    deal_to_company_assocs: List[HubspotDealToCompanyUnique]
    call_to_contact_assocs: List[HubspotCallToContactUnique]


class HubspotAuto(HubspotBase):

    ICON = "hubspot"

    class InitSchema(Node.InitSchema):
        __doc__ = """Will create sync all the relevant data to your HubSpot account."""
        call_properties: str = Field(
            DEFAULT_CALL_PROPERTIES,
            title="Call properties",
            description="The properties to assign to calls (comma separated).",
            json_schema_extra={
                "advanced": True,
                "uiSchema": {
                    "ui:widget": "textarea",
                    "ui:placeholder": f"Comma separated properties, for example: {DEFAULT_CALL_PROPERTIES}",
                },
            },
        )
        company_properties: str = Field(
            DEFAULT_COMPANY_PROPERTIES,
            title="Company properties",
            description="The properties to assign to companies (comma separated).",
            json_schema_extra={
                "advanced": True,
                "uiSchema": {
                    "ui:widget": "textarea",
                    "ui:placeholder": f"Comma separated properties, for example: {DEFAULT_COMPANY_PROPERTIES}",
                },
            },
        )
        contact_properties: str = Field(
            DEFAULT_CONTACT_PROPERTIES,
            title="Contact properties",
            description="The properties to assign to contacts (comma separated).",
            json_schema_extra={
                "advanced": True,
                "uiSchema": {
                    "ui:widget": "textarea",
                    "ui:placeholder": f"Comma separated properties, for example: {DEFAULT_CONTACT_PROPERTIES}",
                },
            },
        )
        deal_properties: str = Field(
            DEFAULT_DEAL_PROPERTIES,
            title="Deal properties",
            description="The properties to assign to deals (comma separated).",
            json_schema_extra={
                "advanced": True,
                "uiSchema": {
                    "ui:widget": "textarea",
                    "ui:placeholder": f"Comma separated properties, for example: {DEFAULT_DEAL_PROPERTIES}",
                },
            },
        )

        update_companies_if_exist: bool = Field(
            True,
            title="Update companies if exist",
            json_schema_extra={"advanced": True},
        )
        update_contacts_if_exist: bool = Field(
            True,
            title="Update contacts if exist",
            json_schema_extra={"advanced": True},
        )
        update_deals_if_exist: bool = Field(
            True,
            title="Update deals if exist",
            json_schema_extra={"advanced": True},
        )

        @field_validator("company_properties")
        def validate_company_properties(cls, v):
            return validate_properties_generic(v, REQUIRED_COMPANY_PROPERTIES)

        @field_validator("contact_properties")
        def validate_contact_properties(cls, v):
            return validate_properties_generic(v, REQUIRED_CONTACT_PROPERTIES)

        @field_validator("deal_properties")
        def validate_deal_properties(cls, v):
            return validate_properties_generic(v, REQUIRED_DEAL_PROPERTIES)

        @field_validator("call_properties")
        def validate_call_properties(cls, v):
            return validate_properties_generic(v, REQUIRED_CALL_PROPERTIES)

    DESC = InitSchema.__doc__

    class InputSchema(Node.InputSchema):
        model_config = ConfigDict(use_enum_values=True)
        input: HubSpotAutoEntity = Field(
            ...,
            title="Input",
            description="The different HubSpot entities to create or update.",
            json_schema_extra={"type-friendly": "HubSpot Auto Entity"},
        )

    class OutputSchema(Node.OutputSchema):
        actions_report: str = Field(
            "",
            title="Actions Report",
            description="The actions that were performed.",
            json_schema_extra={"uiSchema": {"ui:widget": "textarea"}},
        )

    def __init__(self, init_inputs: InitSchema):
        self._call_properties = init_inputs.call_properties
        self._company_properties = init_inputs.company_properties
        self._contact_properties = init_inputs.contact_properties
        self._deal_properties = init_inputs.deal_properties
        self.update_companies_if_exist = init_inputs.update_companies_if_exist
        self.update_contacts_if_exist = init_inputs.update_contacts_if_exist
        self.update_deals_if_exist = init_inputs.update_deals_if_exist
        super().__init__(init_inputs)

    @property
    def call_properties(self):
        return self._call_properties

    @call_properties.setter
    def call_properties(self, value):
        self._call_properties = value
        self._set_schemas()

    @property
    def company_properties(self):
        return self._company_properties

    @company_properties.setter
    def company_properties(self, value):
        self._company_properties = value
        self._set_schemas()

    @property
    def contact_properties(self):
        return self._contact_properties

    @contact_properties.setter
    def contact_properties(self, value):
        self._contact_properties = value
        self._set_schemas()

    @property
    def deal_properties(self):
        return self._deal_properties

    @deal_properties.setter
    def deal_properties(self, value):
        self._deal_properties = value
        self._set_schemas()

    def serialize(self):
        return super().serialize() | {
            "call_properties": self.call_properties,
            "company_properties": self.company_properties,
            "contact_properties": self.contact_properties,
            "deal_properties": self.deal_properties,
            "update_companies_if_exist": self.update_companies_if_exist,
            "update_contacts_if_exist": self.update_contacts_if_exist,
            "update_deals_if_exist": self.update_deals_if_exist,
        }

    def associate_call_to_contact(self, assoc, calls, contacts):
        actions = []
        call = calls.get(
            assoc.hs_call_title,
            HubspotCallCreate.get_existing(self.service, assoc.hs_call_title),
        )
        contact = contacts.get(
            assoc.contact_email,
            HubspotContactCreate.get_existing(self.service, assoc.contact_email),
        )
        if contact:
            assoc = ContactToCall(to=AssociationTo(id=call.id))
            assoc_entity = HubspotContactCreate.associate(
                self.service, contact.id, assoc
            )
            if assoc_entity:
                actions.append(
                    f"Contact {contact.properties['email']} associated with call {call.properties['hs_call_title']}"
                )
                logger.debug(f"Associated contact {contact.id} with call {call.id}")
        else:
            if not contact:
                logger.debug(f"Contact not found for association: {assoc}")
            if not call:
                logger.debug(f"Call not found for association: {assoc}")
        return actions

    def associate_contact_to_company(self, assoc, contacts, companies):
        actions = []
        contact = contacts.get(
            assoc.contact_email,
            HubspotContactCreate.get_existing(self.service, assoc.contact_email),
        )
        company = companies.get(
            assoc.company_domain,
            HubspotCompanyCreate.get_existing(self.service, assoc.company_domain),
        )

        if contact and company:
            assoc = ContactToCompany(to=AssociationTo(id=company.id))
            assoc_entity = HubspotContactCreate.associate(
                self.service, contact.id, assoc
            )
            if assoc_entity:
                actions.append(
                    f"Contact {contact.properties['email']} associated with company {company.properties['domain']}"
                )
                logger.debug(
                    f"Associated contact {contact.id} with company {company.id}"
                )
        else:
            if not contact:
                logger.debug(f"Contact not found for association: {assoc}")
            if not company:
                logger.debug(f"Company not found for association: {assoc}")
        return actions

    def associate_deal_to_company(self, assoc, deals, companies):
        actions = []
        deal = deals.get(
            assoc.dealname,
            HubspotContactCreate.get_existing(self.service, assoc.dealname),
        )
        company = companies.get(
            assoc.company_domain,
            HubspotCompanyCreate.get_existing(self.service, assoc.company_domain),
        )

        if deal and company:
            assoc = DealToCompany(to=AssociationTo(id=company.id))
            assoc_entity = HubspotDealCreate.associate(self.service, deal.id, assoc)
            if assoc_entity:
                actions.append(
                    f"Deal {deal.properties['dealname']} associated with company {company.properties['domain']}"
                )
                logger.debug(f"Associated deal {deal.id} with company {company.id}")
        else:
            if not deal:
                logger.debug(f"Deal not found for association: {assoc}")
            if not company:
                logger.debug(f"Company not found for association: {assoc}")
        return actions

    @classmethod
    def get_entity_create_kls(cls, object_type):
        if object_type == HubspotObjectType.CALL:
            return HubspotCallCreate
        if object_type == HubspotObjectType.COMPANY:
            return HubspotCompanyCreate
        if object_type == HubspotObjectType.CONTACT:
            return HubspotContactCreate
        if object_type == HubspotObjectType.DEAL:
            return HubspotDealCreate
        raise ValueError(f"Unknown object type: {object_type}")

    def create_entities(self, object_type, unique_name, entities, update_if_exists):
        actions = []
        out_entities = {}
        obj_type_name = object_type.value.title()
        create_kls = self.get_entity_create_kls(object_type)

        for entity in entities:
            out_entity, is_update = create_kls.create_or_update_entity(
                self.service,
                entity,
                # add prefix to make unique
                update_if_exists=update_if_exists,
            )
            if not out_entity:
                continue

            unique_val = out_entity.properties[unique_name]
            if unique_val in out_entities:
                logger.error(
                    f"{obj_type_name} with {unique_name} {unique_val} already exists."
                )
            out_entities[unique_val] = out_entity

            if is_update:
                actions.append(f"{obj_type_name} {unique_val} updated")
            else:
                actions.append(f"{obj_type_name} {unique_val} created")

        return actions, out_entities

    def forward(self, node_inputs: InputSchema):
        actions = []
        call_actions, calls = self.create_entities(
            HubspotObjectType.CALL,
            "hs_call_title",
            node_inputs.input.calls,
            update_if_exists="make_unique",
        )
        actions.extend(call_actions)

        company_actions, companies = self.create_entities(
            HubspotObjectType.COMPANY,
            "domain",
            node_inputs.input.companies,
            update_if_exists=self.update_companies_if_exist,
        )
        actions.extend(company_actions)

        contact_actions, contacts = self.create_entities(
            HubspotObjectType.CONTACT,
            "email",
            node_inputs.input.contacts,
            update_if_exists=self.update_contacts_if_exist,
        )
        actions.extend(contact_actions)

        deal_actions, deals = self.create_entities(
            HubspotObjectType.DEAL,
            "dealname",
            node_inputs.input.deals,
            update_if_exists=self.update_deals_if_exist,
        )
        actions.extend(deal_actions)

        for assoc in node_inputs.input.call_to_contact_assocs:
            for hs_call_title in calls:
                if (
                    hs_call_title.startswith(assoc.hs_call_title)
                    and hs_call_title != assoc.hs_call_title
                    and assoc.hs_call_title not in calls
                ):
                    logger.debug(
                        f"Detected change for call assoc {assoc.hs_call_title=}->{hs_call_title}"
                    )
                    assoc.hs_call_title = hs_call_title
            actions.extend(self.associate_call_to_contact(assoc, calls, contacts))

        for assoc in node_inputs.input.contact_to_company_assocs:
            actions.extend(
                self.associate_contact_to_company(assoc, contacts, companies)
            )

        for assoc in node_inputs.input.deal_to_company_assocs:
            actions.extend(self.associate_deal_to_company(assoc, deals, companies))

        self.outputs["actions_report"] = (
            "The following HubSpot changes were made:\n" + "\n".join(actions)
        )

    def _set_schemas(self):
        call_entity = HubspotCallCreate.get_entity_model(
            self.call_properties,
            HubspotCallCreate.CREATE_BASE_KLS,
        )
        company_entity = HubspotCompanyCreate.get_entity_model(
            self.company_properties,
            HubspotCompanyCreate.CREATE_BASE_KLS,
            __validators__=get_company_validators(self.company_properties),
        )
        contact_entity = HubspotContactCreate.get_entity_model(
            self.contact_properties, HubspotContactCreate.CREATE_BASE_KLS
        )
        deal_entity = HubspotDealCreate.get_entity_model(
            self.deal_properties, HubspotDealCreate.CREATE_BASE_KLS
        )
        entity = create_model(
            "HubSpotAutoEntity",
            calls=(List[call_entity], Field(...)),
            companies=(List[company_entity], Field(...)),
            contacts=(List[contact_entity], Field(...)),
            deals=(List[deal_entity], Field(...)),
            __base__=HubSpotAutoEntity,
        )
        self.InputSchema = create_model(
            "HubSpotAutoInput",
            input=(entity, Field(...)),
            __base__=Node.InputSchema,
        )


__all__ = [
    "HubspotAuto",
    "HubspotCallsRead",
    "HubspotCallCreate",
    "HubspotContactsRead",
    "HubspotContactCreate",
    "HubspotCompaniesRead",
    "HubspotCompanyCreate",
    "HubspotDealsRead",
    "HubspotDealCreate",
    "HubspotContactToCompany",
]
