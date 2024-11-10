from datetime import datetime
from enum import Enum
from typing import List

from hubspot.crm.companies.models import (
    PublicObjectSearchRequest as CompanyPublicObjectSearchRequest,
)
from hubspot.crm.companies.models import (
    SimplePublicObjectInputForCreate as CompanySimplePublicObjectInputForCreate,
)
from hubspot.crm.contacts import (
    PublicObjectSearchRequest as ContactPublicObjectSearchRequest,
)
from hubspot.crm.contacts import (
    SimplePublicObjectInputForCreate as ContactSimplePublicObjectInputForCreate,
)
from hubspot.crm.deals.models import (
    PublicObjectSearchRequest as DealPublicObjectSearchRequest,
)
from hubspot.crm.deals.models import (
    SimplePublicObjectInputForCreate as DealSimplePublicObjectInputForCreate,
)
from hubspot.crm.objects import PublicObjectSearchRequest, SimplePublicObjectInput
from loguru import logger
from pydantic import BaseModel, ConfigDict, Field, create_model, field_validator

from plurally.models import hubspot_industries
from plurally.models.hs.assocs import (
    Association,
    AssociationTo,
    ContactToCall,
    ContactToCompany,
    DealToCompany,
)
from plurally.models.hs.base import (
    DEFAULT_CALL_PROPERTIES,
    DEFAULT_COMPANY_PROPERTIES,
    DEFAULT_CONTACT_PROPERTIES,
    DEFAULT_DEAL_PROPERTIES,
    REQUIRED_CALL_PROPERTIES,
    REQUIRED_COMPANY_PROPERTIES,
    REQUIRED_CONTACT_PROPERTIES,
    REQUIRED_DEAL_PROPERTIES,
    HubspotBase,
    HubspotEntityCreateBuilder,
    HubspotEntityReadBuilder,
    HubspotModelBase,
    HubspotObjectType,
    associations,
    validate_properties_generic,
)
from plurally.models.hs.task import (
    DEFAULT_TASK_PROPERTIES,
    REQUIRED_TASK_PROPERTIES,
    HubspotTaskCreate,
    HubspotTasksRead,
)
from plurally.models.node import Node


class HubspotDealStage(Enum):
    APPOINTMENT_SCHEDULED = "appointmentscheduled"
    QUALIFIED_TO_BUY = "qualifiedtobuy"
    PRESENTATION_SCHEDULED = "presentationscheduled"
    DECISION_MAKER_BOUGHT_IN = "decisionmakerboughtin"
    CONTRACT_SENT = "contractsent"
    CLOSED_WON = "closedwon"
    CLOSED_LOST = "closedlost"


class HubspotCallCreateModel(HubspotModelBase): ...


class HubspotCallReadModel(HubspotModelBase):
    id: str


class HubspotLeadCreateModel(HubspotModelBase): ...


class HubspotLeadReadModel(HubspotModelBase):
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


_HubspotCallCreate = HubspotEntityCreateBuilder.build(
    "call",
    "hs_call_title",
    DEFAULT_CALL_PROPERTIES,
    "calls",
    HubspotCallCreateModel,
    HubspotCallReadModel,
    SimplePublicObjectInput,
    PublicObjectSearchRequest,
    associations,
    property_types={"hs_timestamp": datetime},
    property_required=REQUIRED_CALL_PROPERTIES,
    # assoc_adapter=get_entity_to_assoc("Call"),
)


class HubspotCallCreate(_HubspotCallCreate):
    pass


_HubspotContactCreate = HubspotEntityCreateBuilder.build(
    "contact",
    "email",
    DEFAULT_CONTACT_PROPERTIES,
    "contacts",
    HubspotContactCreateModel,
    HubspotContactReadModel,
    ContactSimplePublicObjectInputForCreate,
    ContactPublicObjectSearchRequest,
    associations,
    property_required=REQUIRED_CONTACT_PROPERTIES,
    # assoc_adapter=get_entity_to_assoc("Contact"),
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
    HubspotCompanyCreateModel,
    HubspotCompanyReadModel,
    CompanySimplePublicObjectInputForCreate,
    CompanyPublicObjectSearchRequest,
    associations,
    get_validators=get_company_validators,
    property_required=REQUIRED_COMPANY_PROPERTIES,
    # assoc_adapter=get_entity_to_assoc("Company"),
)


class HubspotCompanyCreate(_HubspotCompanyCreate):
    pass


_HubspotDealCreate = HubspotEntityCreateBuilder.build(
    "deal",
    "dealname",
    DEFAULT_DEAL_PROPERTIES,
    "deals",
    HubspotDealCreateModel,
    HubspotDealReadModel,
    DealSimplePublicObjectInputForCreate,
    DealPublicObjectSearchRequest,
    associations,
    property_types={"dealstage": HubspotDealStage, "closedate": datetime},
    property_required=REQUIRED_DEAL_PROPERTIES,
    # assoc_adapter=get_entity_to_assoc("Deal"),
)


class HubspotDealCreate(_HubspotDealCreate):
    pass


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
        task_properties: str = Field(
            DEFAULT_TASK_PROPERTIES,
            title="Task properties",
            description="The properties to assign to tasks (comma separated).",
            json_schema_extra={
                "advanced": True,
                "uiSchema": {
                    "ui:widget": "textarea",
                    "ui:placeholder": f"Comma separated properties, for example: {DEFAULT_TASK_PROPERTIES}",
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

        @field_validator("task_properties")
        def validate_task_properties(cls, v):
            return validate_properties_generic(v, REQUIRED_TASK_PROPERTIES)

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
        self._task_properties = init_inputs.task_properties

        self.update_companies_if_exist = init_inputs.update_companies_if_exist
        self.update_contacts_if_exist = init_inputs.update_contacts_if_exist
        self.update_deals_if_exist = init_inputs.update_deals_if_exist
        super().__init__(init_inputs)

    @property
    def task_properties(self):
        return self._task_properties

    @task_properties.setter
    def task_properties(self, value):
        self._task_properties = value
        self._set_schemas()

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
            "task_properties": self.task_properties,
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
        if object_type == HubspotObjectType.TASK:
            return HubspotTaskCreate
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

        task_actions, tasks = self.create_entities(
            HubspotObjectType.TASK,
            "hs_task_subject",
            node_inputs.input.tasks,
            update_if_exists="make_unique",
        )
        actions.extend(task_actions)

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
        task_entity = HubspotTaskCreate.get_entity_model(
            self.task_properties, HubspotTaskCreate.CREATE_BASE_KLS
        )

        entity = create_model(
            "HubSpotAutoEntity",
            calls=(List[call_entity], Field(...)),
            companies=(List[company_entity], Field(...)),
            contacts=(List[contact_entity], Field(...)),
            deals=(List[deal_entity], Field(...)),
            tasks=(List[task_entity], Field(...)),
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
    "HubspotTasksRead",
    "HubspotTaskCreate",
]
