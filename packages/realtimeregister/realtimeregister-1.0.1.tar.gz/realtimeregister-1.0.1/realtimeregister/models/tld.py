from dataclasses import dataclass
from typing import Optional, List, Dict, Any

@dataclass
class ContactMetadata:
    min: int
    max: int
    required: bool
    organization_required: bool
    organization_allowed: bool

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ContactMetadata':
        return cls(
            min=data['min'],
            max=data['max'],
            required=data['required'],
            organization_required=data['organizationRequired'],
            organization_allowed=data['organizationAllowed']
        )

@dataclass
class NameserverMetadata:
    min: int
    max: int
    required: bool

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'NameserverMetadata':
        return cls(
            min=data['min'],
            max=data['max'],
            required=data['required']
        )

@dataclass
class RegistrantMetadata:
    organization_required: bool
    organization_allowed: bool

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'RegistrantMetadata':
        return cls(
            organization_required=data['organizationRequired'],
            organization_allowed=data['organizationAllowed']
        )

@dataclass
class TLDMetadata:
    registrant: RegistrantMetadata
    add_grace_period: int
    auto_renew_grace_period: int
    renew_grace_period: int
    transfer_grace_period: int
    creation_requires_pre_validation: bool
    transfer_foa: bool
    whois_exposure: str
    gdpr_category: str
    restore_includes_renew: bool
    registrant_change_transfer_lock: bool
    create_domain_periods: List[int]
    custom_authcode_support: bool
    admin_contacts: ContactMetadata
    billing_contacts: ContactMetadata
    tech_contacts: ContactMetadata
    nameservers: NameserverMetadata
    possible_client_domain_statuses: List[str]
    auto_renew_domain_periods: List[int]
    allowed_dnssec_records: int
    allowed_dnssec_algorithms: List[int]
    transfer_domain_periods: List[int]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TLDMetadata':
        return cls(
            registrant=RegistrantMetadata.from_dict(data['registrant']),
            add_grace_period=data['addGracePeriod'],
            auto_renew_grace_period=data['autoRenewGracePeriod'],
            renew_grace_period=data['renewGracePeriod'],
            transfer_grace_period=data['transferGracePeriod'],
            creation_requires_pre_validation=data['creationRequiresPreValidation'],
            transfer_foa=data['transferFOA'],
            whois_exposure=data['whoisExposure'],
            gdpr_category=data['gdprCategory'],
            restore_includes_renew=data['restoreIncludesRenew'],
            registrant_change_transfer_lock=data['registrantChangeTransferLock'],
            create_domain_periods=data['createDomainPeriods'],
            custom_authcode_support=data['customAuthcodeSupport'],
            admin_contacts=ContactMetadata.from_dict(data['adminContacts']),
            billing_contacts=ContactMetadata.from_dict(data['billingContacts']),
            tech_contacts=ContactMetadata.from_dict(data['techContacts']),
            nameservers=NameserverMetadata.from_dict(data['nameservers']),
            possible_client_domain_statuses=data['possibleClientDomainStatuses'],
            auto_renew_domain_periods=data['autoRenewDomainPeriods'],
            allowed_dnssec_records=data['allowedDnssecRecords'],
            allowed_dnssec_algorithms=data['allowedDnssecAlgorithms'],
            transfer_domain_periods=data['transferDomainPeriods']
        )

@dataclass
class TLD:
    metadata: TLDMetadata

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TLD':
        return cls(
            metadata=TLDMetadata.from_dict(data['metadata'])
        )