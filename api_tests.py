import unittest
import settings
from models import *
from api import *
import random
import string
import datetime

numbers = [str(i) for i in range(10)]
letters = list(string.ascii_lowercase)

class TestTenantApi(unittest.TestCase):
    def setUp(self) -> None:
        clear_db()

    def test_tenant_create_and_get(self):
        tenant = {
            'first_name': 'first_name',
            'last_name': 'last_name',
            'phone': '123456789',
            'email': 'test@example.com'
        }
        success, obj = TenantApi.create_tenant(tenant)

        self.assertTrue(success)

        success, obj = TenantApi.get_tenant(obj['id'])

        self.assertEqual(tenant['first_name'], obj['first_name'])
        self.assertEqual(tenant['last_name'], obj['last_name'])
        self.assertEqual(tenant['phone'], obj['phone'])
        self.assertEqual(tenant['email'], obj['email'])

    def test_tenant_list_and_pagination(self):
        # settings.PAGINATION_PAGE_SIZE = 2
        tenant_1 = {
            'first_name': 'first_name1',
            'last_name': 'last_name1',
            'phone': '123456789',
            'email': 'test1@example.com'
        }
        tenant_2 = {
            'first_name': 'first_name2',
            'last_name': 'last_name2',
            'phone': '123456789',
            'email': 'test2@example.com'
        }
        tenant_3 = {
            'first_name': 'first_name3',
            'last_name': 'last_name3',
            'phone': '123456789',
            'email': 'test3@example.com'
        }

        TenantApi.create_tenant(tenant_1)
        TenantApi.create_tenant(tenant_2)
        TenantApi.create_tenant(tenant_3)

        success, result1 = TenantApi.tenant_list()

        self.assertEqual(result1['previous'], None)
        self.assertEqual(type(result1['next']), str)

        success, result2 = TenantApi.tenant_list(final_url=result1['next'])

        self.assertEqual(type(result2['previous']), str)
        self.assertEqual(result2['next'], None)

        self.assertEqual(result2['results'][0]['first_name'], tenant_3['first_name'])
        self.assertEqual(result2['results'][0]['last_name'], tenant_3['last_name'])
        self.assertEqual(result2['results'][0]['phone'], tenant_3['phone'])
        self.assertEqual(result2['results'][0]['email'], tenant_3['email'])

    def test_get_non_existent_tenant(self):
        success, obj = TenantApi.get_tenant(1)
        self.assertFalse(success)

    def test_update_tenant(self):
        tenant = {
            'first_name': 'first_name',
            'last_name': 'last_name',
            'phone': '123456789',
            'email': 'test@example.com'
        }
        success, obj = TenantApi.create_tenant(tenant)

        tenant_new_data = {
            'id': obj['id'],
            'first_name': 'first_name_1',
            'last_name': 'last_name_1',
            'phone': '987654321',
            'email': 'test_1@example.com'
        }

        success, obj = TenantApi.update_tenant(tenant_new_data)

        self.assertTrue(success)

        self.assertEqual(tenant_new_data['first_name'], obj['first_name'])
        self.assertEqual(tenant_new_data['last_name'], obj['last_name'])
        self.assertEqual(tenant_new_data['phone'], obj['phone'])
        self.assertEqual(tenant_new_data['email'], obj['email'])

    def test_filter_tenant_list(self):
        tenant_1 = {
            'first_name': 'first_name1',
            'last_name': 'last_name1',
            'phone': '123456789',
            'email': 'test1@example.com'
        }
        tenant_2 = {
            'first_name': 'first_name2',
            'last_name': 'last_name2',
            'phone': '123456789',
            'email': 'test2@example.com'
        }
        tenant_3 = {
            'first_name': 'first_name3',
            'last_name': 'last_name3',
            'phone': '123456789',
            'email': 'test3@example.com'
        }

        TenantApi.create_tenant(tenant_1)
        TenantApi.create_tenant(tenant_2)
        TenantApi.create_tenant(tenant_3)

        success, result = TenantApi.tenant_list('first_name3,last_name3')

        self.assertEqual(len(result['results']), 1)
        self.assertEqual(result['previous'], None)
        self.assertEqual(result['next'], None)

        self.assertEqual(result['results'][0]['first_name'], tenant_3['first_name'])
        self.assertEqual(result['results'][0]['last_name'], tenant_3['last_name'])
        self.assertEqual(result['results'][0]['phone'], tenant_3['phone'])
        self.assertEqual(result['results'][0]['email'], tenant_3['email'])

    def test_filter_tenant_list_by_status(self):
        tenant_1 = {
            'first_name': 'first_name1',
            'last_name': 'last_name1',
            'phone': '123456789',
            'email': 'test1@example.com'
        }
        tenant_2 = {
            'first_name': 'first_name2',
            'last_name': 'last_name2',
            'phone': '123456789',
            'email': 'test2@example.com'
        }
        tenant_3 = {
            'first_name': 'first_name3',
            'last_name': 'last_name3',
            'phone': '000000000',
            'email': 'test3@example.com'
        }
        
        TenantApi.create_tenant(tenant_1)
        TenantApi.create_tenant(tenant_2)
        success, tenant = TenantApi.create_tenant(tenant_3)

        owner = {
            'first_name': 'first_name',
            'last_name': 'last_name',
            'phone': '123456789',
            'email': 'test@example.com'
        }
        success, owner = OwnerApi.create_owner(owner)

        apartment = {
            'name': 'apartment',
            'address': 'address',
            'beds': 10,
            'owner': owner
        }
        success, apartment = ApartmentApi.create_apartment(apartment)

        lease_contract = {
            'start_date': '2023-10-01',
            'end_date': '2023-10-30',
            'rent_price': 800,
            'utilities_included': True,
            'tax': 10,
            'tenant': tenant,
            'apartment': apartment
        }
        success, obj = LeaseContractApi.create_lease_contract(lease_contract)

        success, result = TenantApi.tenant_list(status='active')

        self.assertEqual(len(result['results']), 1)
        self.assertEqual(result['previous'], None)
        self.assertEqual(result['next'], None)

        self.assertEqual(result['results'][0]['first_name'], tenant_3['first_name'])
        self.assertEqual(result['results'][0]['last_name'], tenant_3['last_name'])
        self.assertEqual(result['results'][0]['phone'], tenant_3['phone'])
        self.assertEqual(result['results'][0]['email'], tenant_3['email'])


class TestOwnerApi(unittest.TestCase):
    def setUp(self) -> None:
        clear_db()

    def test_owner_create_and_get(self):
        owner = {
            'first_name': 'first_name',
            'last_name': 'last_name',
            'phone': '123456789',
            'email': 'test@example.com'
        }
        success, obj = OwnerApi.create_owner(owner)

        self.assertTrue(success)

        success, obj = OwnerApi.get_owner(obj['id'])

        self.assertEqual(owner['first_name'], obj['first_name'])
        self.assertEqual(owner['last_name'], obj['last_name'])
        self.assertEqual(owner['phone'], obj['phone'])
        self.assertEqual(owner['email'], obj['email'])

    def test_owner_list_and_pagination(self):
        # settings.PAGINATION_PAGE_SIZE = 2
        owner_1 = {
            'first_name': 'first_name1',
            'last_name': 'last_name1',
            'phone': '123456789',
            'email': 'test1@example.com'
        }
        owner_2 = {
            'first_name': 'first_name2',
            'last_name': 'last_name2',
            'phone': '123456789',
            'email': 'test2@example.com'
        }
        owner_3 = {
            'first_name': 'first_name3',
            'last_name': 'last_name3',
            'phone': '123456789',
            'email': 'test3@example.com'
        }

        OwnerApi.create_owner(owner_1)
        OwnerApi.create_owner(owner_2)
        OwnerApi.create_owner(owner_3)

        success, result1 = OwnerApi.owner_list()

        self.assertEqual(result1['previous'], None)
        self.assertEqual(type(result1['next']), str)

        success, result2 = OwnerApi.owner_list(final_url=result1['next'])

        self.assertEqual(type(result2['previous']), str)
        self.assertEqual(result2['next'], None)

        self.assertEqual(result2['results'][0]['first_name'], owner_3['first_name'])
        self.assertEqual(result2['results'][0]['last_name'], owner_3['last_name'])
        self.assertEqual(result2['results'][0]['phone'], owner_3['phone'])
        self.assertEqual(result2['results'][0]['email'], owner_3['email'])

    def test_get_non_existent_owner(self):
        success, obj = OwnerApi.get_owner(1)
        self.assertFalse(success)

    def test_update_owner(self):
        owner = {
            'first_name': 'first_name',
            'last_name': 'last_name',
            'phone': '123456789',
            'email': 'test@example.com'
        }
        success, obj = OwnerApi.create_owner(owner)

        owner_new_data = {
            'id': obj['id'],
            'first_name': 'first_name_1',
            'last_name': 'last_name_1',
            'phone': '987654321',
            'email': 'test_1@example.com'
        }

        success, obj = OwnerApi.update_owner(owner_new_data)

        self.assertTrue(success)

        self.assertEqual(owner_new_data['first_name'], obj['first_name'])
        self.assertEqual(owner_new_data['last_name'], obj['last_name'])
        self.assertEqual(owner_new_data['phone'], obj['phone'])
        self.assertEqual(owner_new_data['email'], obj['email'])

    def test_filter_owner_list(self):
        owner_1 = {
            'first_name': 'first_name1',
            'last_name': 'last_name1',
            'phone': '123456789',
            'email': 'test1@example.com'
        }
        owner_2 = {
            'first_name': 'first_name2',
            'last_name': 'last_name2',
            'phone': '123456789',
            'email': 'test2@example.com'
        }
        owner_3 = {
            'first_name': 'first_name3',
            'last_name': 'last_name3',
            'phone': '123456789',
            'email': 'test3@example.com'
        }

        OwnerApi.create_owner(owner_1)
        OwnerApi.create_owner(owner_2)
        OwnerApi.create_owner(owner_3)

        success, result = OwnerApi.owner_list('test3')

        self.assertEqual(len(result['results']), 1)
        self.assertEqual(result['previous'], None)
        self.assertEqual(result['next'], None)

        self.assertEqual(result['results'][0]['first_name'], owner_3['first_name'])
        self.assertEqual(result['results'][0]['last_name'], owner_3['last_name'])
        self.assertEqual(result['results'][0]['phone'], owner_3['phone'])
        self.assertEqual(result['results'][0]['email'], owner_3['email'])


class TestApartmentApi(unittest.TestCase):
    def setUp(self) -> None:
        clear_db()

    def test_apartment_create_and_get(self):
        owner = {
            'first_name': 'first_name',
            'last_name': 'last_name',
            'phone': '123456789',
            'email': 'test@example.com'
        }
        success, obj = OwnerApi.create_owner(owner)

        apartment = {
            'name': 'apartment',
            'address': 'address',
            'beds': 10,
            'owner': obj
        }

        success, obj = ApartmentApi.create_apartment(apartment)

        self.assertTrue(success)

        success, obj = ApartmentApi.get_apartment(obj['id'])

        self.assertEqual(apartment['name'], obj['name'])
        self.assertEqual(apartment['address'], obj['address'])
        self.assertEqual(apartment['beds'], obj['beds'])
        self.assertEqual(apartment['owner'], obj['owner'])

    def test_apartment_list_and_pagination(self):
        # settings.PAGINATION_PAGE_SIZE = 2
        owner = {
            'first_name': 'first_name',
            'last_name': 'last_name',
            'phone': '123456789',
            'email': 'test@example.com'
        }
        success, obj = OwnerApi.create_owner(owner)
    
        apartment_1 = {
            'name': 'apartment 1',
            'address': 'address 1',
            'beds': 1,
            'owner': obj
        }
        apartment_2 = {
            'name': 'apartment 2',
            'address': 'address 2',
            'beds': 2,
            'owner': obj
        }
        apartment_3 = {
            'name': 'apartment 3',
            'address': 'address 3',
            'beds': 3,
            'owner': obj
        }

        ApartmentApi.create_apartment(apartment_1)
        ApartmentApi.create_apartment(apartment_2)
        ApartmentApi.create_apartment(apartment_3)

        success, result1 = ApartmentApi.apartment_list()

        self.assertEqual(result1['previous'], None)
        self.assertEqual(type(result1['next']), str)

        success, result2 = ApartmentApi.apartment_list(final_url=result1['next'])

        self.assertEqual(type(result2['previous']), str)
        self.assertEqual(result2['next'], None)

        self.assertEqual(result2['results'][0]['name'], apartment_3['name'])
        self.assertEqual(result2['results'][0]['address'], apartment_3['address'])
        self.assertEqual(result2['results'][0]['beds'], apartment_3['beds'])
        self.assertEqual(result2['results'][0]['owner'], obj)

    def test_get_non_existent_apartment(self):
        success, obj = ApartmentApi.get_apartment(1)
        self.assertFalse(success)

    def test_update_apartment(self):
        owner_1 = {
            'first_name': 'first_name1',
            'last_name': 'last_name1',
            'phone': '123456789',
            'email': 'test1@example.com'
        }
        owner_2 = {
            'first_name': 'first_name2',
            'last_name': 'last_name2',
            'phone': '987654321',
            'email': 'test2@example.com'
        }
        success, owner_1 = OwnerApi.create_owner(owner_1)
        success, owner_2 = OwnerApi.create_owner(owner_2)

        apartment = {
            'name': 'apartment',
            'address': 'address',
            'beds': 1,
            'owner': owner_1
        }

        success, obj = ApartmentApi.create_apartment(apartment)

        apartment_new_data = {
            'id': obj['id'],
            'name': 'apartment 1',
            'address': 'address 1',
            'beds': 2,
            'owner': owner_2
        }

        success, obj = ApartmentApi.update_apartment(apartment_new_data)

        self.assertTrue(success)

        self.assertEqual(apartment_new_data['name'], obj['name'])
        self.assertEqual(apartment_new_data['address'], obj['address'])
        self.assertEqual(apartment_new_data['beds'], obj['beds'])
        self.assertEqual(apartment_new_data['owner'], owner_2)

    def test_filter_apartment_list(self):
        owner_1 = {
            'first_name': 'first_name1',
            'last_name': 'last_name1',
            'phone': '123456789',
            'email': 'test1@example.com'
        }
        owner_2 = {
            'first_name': 'first_name2',
            'last_name': 'last_name2',
            'phone': '123456789',
            'email': 'test2@example.com'
        }

        success, owner_1 = OwnerApi.create_owner(owner_1)
        success, owner_2 = OwnerApi.create_owner(owner_2)

        apartment_1 = {
            'name': 'apartment 1',
            'address': 'address 1',
            'beds': 1,
            'owner': owner_1
        }
        apartment_2 = {
            'name': 'apartment 2',
            'address': 'address 2',
            'beds': 2,
            'owner': owner_1
        }
        apartment_3 = {
            'name': 'apartment 3',
            'address': 'address 3',
            'beds': 3,
            'owner': owner_2
        }

        ApartmentApi.create_apartment(apartment_1)
        ApartmentApi.create_apartment(apartment_2)
        ApartmentApi.create_apartment(apartment_3)

        success, result = ApartmentApi.apartment_list('test2')

        self.assertEqual(len(result['results']), 1)
        self.assertEqual(result['previous'], None)
        self.assertEqual(result['next'], None)

        self.assertEqual(result['results'][0]['name'], apartment_3['name'])
        self.assertEqual(result['results'][0]['address'], apartment_3['address'])
        self.assertEqual(result['results'][0]['beds'], apartment_3['beds'])
        self.assertEqual(result['results'][0]['owner'], owner_2)


class TestLeaseContractApi(unittest.TestCase):
    def setUp(self) -> None:
        clear_db()

    def test_lease_contract_create_and_get(self):
        owner = {
            'first_name': 'first_name',
            'last_name': 'last_name',
            'phone': '123456789',
            'email': 'test@example.com'
        }
        tenant = {
            'first_name': 'first_name',
            'last_name': 'last_name',
            'phone': '123456789',
            'email': 'test@example.com'
        }

        success, tenant = TenantApi.create_tenant(tenant)
        success, owner = OwnerApi.create_owner(owner)

        apartment = {
            'name': 'apartment',
            'address': 'address',
            'beds': 10,
            'owner': owner
        }
        success, apartment = ApartmentApi.create_apartment(apartment)

        lease_contract = {
            'start_date': '2023-10-01',
            'end_date': '2023-10-30',
            'rent_price': 800,
            'utilities_included': True,
            'tax': 10,
            'tenant': tenant,
            'apartment': apartment
        }
        success, obj = LeaseContractApi.create_lease_contract(lease_contract)

        self.assertTrue(success)

        success, obj = LeaseContractApi.get_lease_contract(obj['id'])

        self.assertEqual(lease_contract['start_date'], obj['start_date'])
        self.assertEqual(lease_contract['end_date'], obj['end_date'])
        self.assertEqual(lease_contract['rent_price'], obj['rent_price'])
        self.assertEqual(lease_contract['utilities_included'], obj['utilities_included'])
        self.assertEqual(lease_contract['tax'], obj['tax'])
        self.assertNotEqual(lease_contract['tenant'], obj['tenant'])
        self.assertEqual(lease_contract['apartment'], obj['apartment'])

    def test_lease_contract_list_and_pagination(self):
        # settings.PAGINATION_PAGE_SIZE = 2
        owner = {
            'first_name': 'first_name',
            'last_name': 'last_name',
            'phone': '123456789',
            'email': 'test@example.com'
        }
        tenant = {
            'first_name': 'first_name',
            'last_name': 'last_name',
            'phone': '123456789',
            'email': 'test@example.com'
        }

        success, tenant = TenantApi.create_tenant(tenant)
        success, owner = OwnerApi.create_owner(owner)

        apartment = {
            'name': 'apartment',
            'address': 'address',
            'beds': 10,
            'owner': owner
        }
        success, apartment = ApartmentApi.create_apartment(apartment)

        lease_contract_1 = {
            'start_date': '2023-10-01',
            'end_date': '2023-10-30',
            'rent_price': 1,
            'utilities_included': True,
            'tax': 1,
            'tenant': tenant,
            'apartment': apartment
        }
        lease_contract_2 = {
            'start_date': '2023-11-01',
            'end_date': '2023-11-30',
            'rent_price': 2,
            'utilities_included': True,
            'tax': 2,
            'tenant': tenant,
            'apartment': apartment
        }
        lease_contract_3 = {
            'start_date': '2023-12-01',
            'end_date': '2023-12-30',
            'rent_price': 3,
            'utilities_included': True,
            'tax': 3,
            'tenant': tenant,
            'apartment': apartment
        }

        LeaseContractApi.create_lease_contract(lease_contract_1)
        LeaseContractApi.create_lease_contract(lease_contract_2)
        LeaseContractApi.create_lease_contract(lease_contract_3)

        success, result1 = LeaseContractApi.lease_contract_list()

        self.assertEqual(result1['previous'], None)
        self.assertEqual(type(result1['next']), str)

        success, result2 = LeaseContractApi.lease_contract_list(final_url=result1['next'])

        self.assertEqual(type(result2['previous']), str)
        self.assertEqual(result2['next'], None)

        self.assertEqual(result2['results'][0]['start_date'], lease_contract_1['start_date'])
        self.assertEqual(result2['results'][0]['end_date'], lease_contract_1['end_date'])
        self.assertEqual(result2['results'][0]['rent_price'], lease_contract_1['rent_price'])
        self.assertEqual(result2['results'][0]['utilities_included'], lease_contract_1['utilities_included'])
        self.assertEqual(result2['results'][0]['tax'], lease_contract_1['tax'])
        self.assertNotEqual(result2['results'][0]['tenant'], lease_contract_1['tenant'])
        self.assertEqual(result2['results'][0]['apartment'], lease_contract_1['apartment'])

    def test_get_non_existent_lease_contract(self):
        success, obj = LeaseContractApi.get_lease_contract(1)
        self.assertFalse(success)

    def test_update_lease_contract(self):
        owner = {
            'first_name': 'first_name',
            'last_name': 'last_name',
            'phone': '123456789',
            'email': 'test@example.com'
        }
        tenant = {
            'first_name': 'first_name',
            'last_name': 'last_name',
            'phone': '123456789',
            'email': 'test@example.com'
        }

        success, tenant = TenantApi.create_tenant(tenant)
        success, owner = OwnerApi.create_owner(owner)

        apartment = {
            'name': 'apartment',
            'address': 'address',
            'beds': 10,
            'owner': owner
        }
        success, apartment = ApartmentApi.create_apartment(apartment)

        lease_contract = {
            'start_date': '2023-10-01',
            'end_date': '2023-10-30',
            'rent_price': 800,
            'utilities_included': True,
            'tax': 10,
            'tenant': tenant,
            'apartment': apartment
        }
        success, obj = LeaseContractApi.create_lease_contract(lease_contract)

        lease_contract_new_data = {
            'id': obj['id'],
            'start_date': '2023-11-01',
            'end_date': '2023-11-30',
            'rent_price': 1200,
            'utilities_included': False,
            'tax': 100,
            'tenant': tenant,
            'apartment': apartment
        }

        success, obj = LeaseContractApi.update_lease_contract(lease_contract_new_data)

        self.assertTrue(success)

        self.assertEqual(lease_contract_new_data['start_date'], obj['start_date'])
        self.assertEqual(lease_contract_new_data['end_date'], obj['end_date'])
        self.assertEqual(lease_contract_new_data['rent_price'], obj['rent_price'])
        self.assertEqual(lease_contract_new_data['utilities_included'], obj['utilities_included'])
        self.assertEqual(lease_contract_new_data['tax'], obj['tax'])
        self.assertEqual(lease_contract_new_data['tenant'], obj['tenant'])
        self.assertEqual(lease_contract_new_data['apartment'], obj['apartment'])

    def test_filter_lease_contract_list(self):
        owner_1 = {
            'first_name': 'first_name1',
            'last_name': 'last_name1',
            'phone': '123456789',
            'email': 'test1@example.com'
        }
        owner_2 = {
            'first_name': 'first_name2',
            'last_name': 'last_name2',
            'phone': '123456789',
            'email': 'test2@example.com'
        }
        tenant = {
            'first_name': 'first_name',
            'last_name': 'last_name',
            'phone': '123456789',
            'email': 'test@example.com'
        }

        success, tenant = TenantApi.create_tenant(tenant)
        success, owner_1 = OwnerApi.create_owner(owner_1)
        success, owner_2 = OwnerApi.create_owner(owner_2)

        apartment_1 = {
            'name': 'apartment1',
            'address': 'address1',
            'beds': 1,
            'owner': owner_1
        }
        apartment_2 = {
            'name': 'apartment2',
            'address': 'address2',
            'beds': 2,
            'owner': owner_2
        }
        success, apartment_1 = ApartmentApi.create_apartment(apartment_1)
        success, apartment_2 = ApartmentApi.create_apartment(apartment_2)

        lease_contract_1 = {
            'start_date': '2023-10-01',
            'end_date': '2023-10-30',
            'rent_price': 1,
            'utilities_included': True,
            'tax': 1,
            'tenant': tenant,
            'apartment': apartment_1
        }
        lease_contract_2 = {
            'start_date': '2023-11-01',
            'end_date': '2023-11-30',
            'rent_price': 2,
            'utilities_included': True,
            'tax': 2,
            'tenant': tenant,
            'apartment': apartment_1
        }
        lease_contract_3 = {
            'start_date': '2023-12-01',
            'end_date': '2023-12-30',
            'rent_price': 1331,
            'utilities_included': True,
            'tax': 3,
            'tenant': tenant,
            'apartment': apartment_2
        }

        LeaseContractApi.create_lease_contract(lease_contract_1)
        LeaseContractApi.create_lease_contract(lease_contract_2)
        LeaseContractApi.create_lease_contract(lease_contract_3)

        success, result = LeaseContractApi.lease_contract_list('test2')

        self.assertEqual(len(result['results']), 1)
        self.assertEqual(result['previous'], None)
        self.assertEqual(result['next'], None)
        # result['results'][0]['tenant'].pop('status')

        self.assertEqual(result['results'][0]['start_date'], lease_contract_3['start_date'])
        self.assertEqual(result['results'][0]['end_date'], lease_contract_3['end_date'])
        self.assertEqual(result['results'][0]['rent_price'], lease_contract_3['rent_price'])
        self.assertEqual(result['results'][0]['utilities_included'], lease_contract_3['utilities_included'])
        self.assertEqual(result['results'][0]['tax'], lease_contract_3['tax'])
        self.assertNotEqual(result['results'][0]['tenant'], lease_contract_3['tenant'])
        self.assertEqual(result['results'][0]['apartment'], lease_contract_3['apartment'])
  
    def test_filter_lease_contract_list_by_active(self):
        owner_1 = {
            'first_name': 'first_name1',
            'last_name': 'last_name1',
            'phone': '123456789',
            'email': 'test1@example.com'
        }
        owner_2 = {
            'first_name': 'first_name2',
            'last_name': 'last_name2',
            'phone': '123456789',
            'email': 'test2@example.com'
        }
        tenant = {
            'first_name': 'first_name',
            'last_name': 'last_name',
            'phone': '123456789',
            'email': 'test@example.com'
        }

        success, tenant = TenantApi.create_tenant(tenant)
        success, owner_1 = OwnerApi.create_owner(owner_1)
        success, owner_2 = OwnerApi.create_owner(owner_2)

        apartment_1 = {
            'name': 'apartment1',
            'address': 'address1',
            'beds': 1,
            'owner': owner_1
        }
        apartment_2 = {
            'name': 'apartment2',
            'address': 'address2',
            'beds': 2,
            'owner': owner_2
        }
        success, apartment_1 = ApartmentApi.create_apartment(apartment_1)
        success, apartment_2 = ApartmentApi.create_apartment(apartment_2)

        lease_contract_1 = {
            'start_date': '2022-10-01',
            'end_date': '2022-10-30',
            'rent_price': 1,
            'utilities_included': True,
            'tax': 1,
            'tenant': tenant,
            'apartment': apartment_1
        }
        lease_contract_2 = {
            'start_date': (datetime.datetime.now() + datetime.timedelta(days=30)).date().strftime('%Y-%m-%d'),
            'end_date': '2023-11-30',
            'rent_price': 2,
            'utilities_included': True,
            'tax': 2,
            'tenant': tenant,
            'apartment': apartment_1
        }
        lease_contract_3 = {
            'start_date': '2022-12-01',
            'end_date': '2022-12-30',
            'rent_price': 1331,
            'utilities_included': True,
            'tax': 3,
            'tenant': tenant,
            'apartment': apartment_2
        }

        LeaseContractApi.create_lease_contract(lease_contract_1)
        LeaseContractApi.create_lease_contract(lease_contract_2)
        LeaseContractApi.create_lease_contract(lease_contract_3)

        success, result = LeaseContractApi.lease_contract_list(active=True)

        self.assertEqual(len(result['results']), 1)
        self.assertEqual(result['previous'], None)
        self.assertEqual(result['next'], None)

        self.assertEqual(result['results'][0]['start_date'], lease_contract_2['start_date'])
        self.assertEqual(result['results'][0]['end_date'], lease_contract_2['end_date'])
        self.assertEqual(result['results'][0]['rent_price'], lease_contract_2['rent_price'])
        self.assertEqual(result['results'][0]['utilities_included'], lease_contract_2['utilities_included'])
        self.assertEqual(result['results'][0]['tax'], lease_contract_2['tax'])
        self.assertEqual(result['results'][0]['tenant'], lease_contract_2['tenant'])
        self.assertEqual(result['results'][0]['apartment'], lease_contract_2['apartment'])


class TestTransactionApi(unittest.TestCase):
    def setUp(self) -> None:
        Transaction.delete().execute()
        LeaseContract.delete().execute()
        Owner.delete().execute()
        Apartment.delete().execute()
        Tenant.delete().execute()
        UtilityBills.delete().execute()
    
    def create_LeaseContract(self):
        tenant = {
            'first_name': ''.join([random.choice(letters) for i in range(10)]),
            'last_name': ''.join([random.choice(letters) for i in range(10)]),
            'phone': ''.join([random.choice(numbers) for i in range(10)]),
            'email': ''.join([random.choice(letters) for i in range(10)]) + '@example.com'
        }
        owner = {
            'first_name': ''.join([random.choice(letters) for i in range(10)]),
            'last_name': ''.join([random.choice(letters) for i in range(10)]),
            'phone': ''.join([random.choice(numbers) for i in range(10)]),
            'email': ''.join([random.choice(letters) for i in range(10)]) + '@example.com'
        }

        success, tenant = TenantApi.create_tenant(tenant)
        success, owner = OwnerApi.create_owner(owner)

        apartment = {
            'name': 'apartment',
            'address': 'address',
            'beds': 10,
            'owner': owner
        }
        success, apartment = ApartmentApi.create_apartment(apartment)

        lease_contract = {
            'start_date': '2023-10-01',
            'end_date': '2023-10-30',
            'rent_price': 800,
            'utilities_included': True,
            'tax': 10,
            'tenant': tenant,
            'apartment': apartment
        }
        success, obj = LeaseContractApi.create_lease_contract(lease_contract)

        return obj

    def test_transaction_create_and_get(self):
        transaction = {
            'date': '2023-10-01',
            'transaction_type': 'utility_payment',
            'amount': 30,
            'category': 'otner',
            'lease_contract': self.create_LeaseContract(),
            'utility_bills': {
                'water': 10,
                'electricity': 10,
                'tax': 10,
            }
        }
        success, obj = TransactionApi.create_transaction(transaction)

        self.assertTrue(success)

        success, obj = TransactionApi.get_transaction(obj['id'])
        obj['utility_bills'].pop('id')

        self.assertEqual(transaction['date'], obj['date'])
        self.assertEqual(transaction['transaction_type'], obj['transaction_type'])
        self.assertEqual(transaction['amount'], obj['amount'])
        self.assertEqual(transaction['category'], obj['category'])
        self.assertEqual(transaction['lease_contract'], obj['lease_contract'])

    def test_transaction_list_and_pagination(self):
        # settings.PAGINATION_PAGE_SIZE = 2
        transaction_1 = {
            'date': '2023-10-01',
            'transaction_type': 'income',
            'amount': 1,
            'category': 'otner',
            'lease_contract': self.create_LeaseContract()
        }
        transaction_2 = {
            'date': '2023-10-02',
            'transaction_type': 'income',
            'amount': 2,
            'category': 'otner',
            'lease_contract': self.create_LeaseContract()
        }
        transaction_3 = {
            'date': '2023-10-03',
            'transaction_type': 'income',
            'amount': 3,
            'category': 'otner',
            'lease_contract': self.create_LeaseContract()
        }

        TransactionApi.create_transaction(transaction_1)
        TransactionApi.create_transaction(transaction_2)
        TransactionApi.create_transaction(transaction_3)

        success, result1 = TransactionApi.transaction_list()

        self.assertEqual(result1['previous'], None)
        self.assertEqual(type(result1['next']), str)

        success, result2 = TransactionApi.transaction_list(final_url=result1['next'])

        self.assertEqual(type(result2['previous']), str)
        self.assertEqual(result2['next'], None)

        self.assertEqual(result2['results'][0]['date'], transaction_1['date'])
        self.assertEqual(result2['results'][0]['transaction_type'], transaction_1['transaction_type'])
        self.assertEqual(result2['results'][0]['amount'], transaction_1['amount'])
        self.assertEqual(result2['results'][0]['category'], transaction_1['category'])
        self.assertEqual(result2['results'][0]['lease_contract'], transaction_1['lease_contract'])

    def test_get_non_existent_tenant(self):
        success, obj = TransactionApi.get_transaction(1)
        self.assertFalse(success)

    def test_update_transaction(self):
        transaction = {
            'date': '2023-10-01',
            'transaction_type': 'income',
            'amount': 100,
            'category': 'otner',
            'lease_contract': self.create_LeaseContract(),
            'utility_bills': {
                'water': 10,
                'electricity': 10,
                'tax': 10,
            }
        }
        success, obj = TransactionApi.create_transaction(transaction)

        transacton_new_data = {
            'id': obj['id'],
            'date': '2023-10-02',
            'transaction_type': 'expense',
            'amount': 333,
            'category': 'rent_payment',
            'utility_bills': {
                'id': obj['utility_bills']['id'],
                'water': 20,
                'electricity': 20,
                'tax': 20,
            }
        }

        success, obj = TransactionApi.update_transaction(transacton_new_data)

        self.assertTrue(success)
        obj['utility_bills'].pop('id')

        self.assertEqual(transacton_new_data['date'], obj['date'])
        self.assertEqual(transacton_new_data['transaction_type'], obj['transaction_type'])
        self.assertEqual(transacton_new_data['amount'], obj['amount'])
        self.assertEqual(transacton_new_data['category'], obj['category'])
        self.assertEqual(transaction['lease_contract'], obj['lease_contract'])
        self.assertEqual(transacton_new_data['utility_bills'], obj['utility_bills'])


    def test_filter_transaction_list(self):
        transaction_1 = {
            'date': '2023-10-01',
            'transaction_type': 'income',
            'amount': 1,
            'category': 'otner',
            'lease_contract': self.create_LeaseContract()
        }
        transaction_2 = {
            'date': '2023-10-02',
            'transaction_type': 'income',
            'amount': 2,
            'category': 'otner',
            'lease_contract': self.create_LeaseContract()
        }
        transaction_3 = {
            'date': '2023-10-03',
            'transaction_type': 'income',
            'amount': 3,
            'category': 'otner',
            'lease_contract': self.create_LeaseContract()
        }

        TransactionApi.create_transaction(transaction_1)
        TransactionApi.create_transaction(transaction_2)
        TransactionApi.create_transaction(transaction_3)

        success, result = TransactionApi.transaction_list(transaction_2['lease_contract']['tenant']['email'])

        self.assertEqual(len(result['results']), 1)
        self.assertEqual(result['previous'], None)
        self.assertEqual(result['next'], None)

        self.assertEqual(result['results'][0]['date'], transaction_2['date'])
        self.assertEqual(result['results'][0]['transaction_type'], transaction_2['transaction_type'])
        self.assertEqual(result['results'][0]['amount'], transaction_2['amount'])
        self.assertEqual(result['results'][0]['category'], transaction_2['category'])
        self.assertEqual(result['results'][0]['lease_contract'], transaction_2['lease_contract'])

    def test_filter_transaction_list_by_transaction_type(self):
        transaction_1 = {
            'date': '2023-10-01',
            'transaction_type': 'expense',
            'amount': 1,
            'category': 'otner',
            'lease_contract': self.create_LeaseContract()
        }
        transaction_2 = {
            'date': '2023-10-02',
            'transaction_type': 'income',
            'amount': 2,
            'category': 'otner',
            'lease_contract': self.create_LeaseContract()
        }
        transaction_3 = {
            'date': '2023-10-03',
            'transaction_type': 'income',
            'amount': 3,
            'category': 'otner',
            'lease_contract': self.create_LeaseContract()
        }

        TransactionApi.create_transaction(transaction_1)
        TransactionApi.create_transaction(transaction_2)
        TransactionApi.create_transaction(transaction_3)

        success, result = TransactionApi.transaction_list(transaction_type='expense')

        self.assertEqual(len(result['results']), 1)
        self.assertEqual(result['previous'], None)
        self.assertEqual(result['next'], None)

        self.assertEqual(result['results'][0]['date'], transaction_1['date'])
        self.assertEqual(result['results'][0]['transaction_type'], transaction_1['transaction_type'])
        self.assertEqual(result['results'][0]['amount'], transaction_1['amount'])
        self.assertEqual(result['results'][0]['category'], transaction_1['category'])
        self.assertEqual(result['results'][0]['lease_contract'], transaction_1['lease_contract'])


class TestNotificationsApi(unittest.TestCase):
    def setUp(self) -> None:
        Reminder.delete().execute()
        Task.delete().execute()
        NamedDate.delete().execute()
        CellAction.delete().execute()
        LeaseContract.delete().execute()
        Owner.delete().execute()
        Apartment.delete().execute()
        Tenant.delete().execute()
    
    def create_LeaseContract(self):
        tenant = {
            'first_name': ''.join([random.choice(letters) for i in range(10)]),
            'last_name': ''.join([random.choice(letters) for i in range(10)]),
            'phone': ''.join([random.choice(numbers) for i in range(10)]),
            'email': ''.join([random.choice(letters) for i in range(10)]) + '@example.com'
        }
        owner = {
            'first_name': ''.join([random.choice(letters) for i in range(10)]),
            'last_name': ''.join([random.choice(letters) for i in range(10)]),
            'phone': ''.join([random.choice(numbers) for i in range(10)]),
            'email': ''.join([random.choice(letters) for i in range(10)]) + '@example.com'
        }

        success, tenant = TenantApi.create_tenant(tenant)
        success, owner = OwnerApi.create_owner(owner)

        apartment = {
            'name': 'apartment',
            'address': 'address',
            'beds': 10,
            'owner': owner
        }
        success, apartment = ApartmentApi.create_apartment(apartment)

        lease_contract = {
            'start_date': '2023-10-01',
            'end_date': '2023-10-30',
            'rent_price': 800,
            'utilities_included': True,
            'tax': 10,
            'tenant': tenant,
            'apartment': apartment
        }
        success, obj = LeaseContractApi.create_lease_contract(lease_contract)

        return obj

    def test_reminder_create_and_get(self):
        reminder = {
            'date': '2023-10-01',
            'text': 'reminder 1',
            'dates': [{'date': '2023-10-02T00:00:00', 'name': 'date_1'}, {'date': '2023-10-03T00:00:00', 'name': 'date_2'}],
            'lease_contract': self.create_LeaseContract(),
        }
        success, obj = NotificationsApi.create_reminder(reminder)

        self.assertTrue(success)

        success, obj = NotificationsApi.get_reminder(obj['id'])
        
        for named_date in obj['dates']:
            named_date.pop('id')

        self.assertEqual(reminder['date'], obj['date'])
        self.assertEqual(reminder['text'], obj['text'])
        self.assertEqual(reminder['dates'], obj['dates'])
        self.assertEqual(reminder['lease_contract'], obj['lease_contract'])

    def test_task_create_and_get(self):
        task = {
            'date': '2023-10-01',
            'text': 'task 1',
            'note': 'some Note',
            'dates': [{'date': '2023-10-02T00:00:00', 'name': 'date_1'}, {'date': '2023-10-03T00:00:00', 'name': 'date_2'}],
            'actions': [{'action': 'acton_1', 'done': False}],
            'lease_contract': self.create_LeaseContract(),
        }
        success, obj = NotificationsApi.create_task(task)

        self.assertTrue(success)

        success, obj = NotificationsApi.get_task(obj['id'])

        for named_date in obj['dates']:
            named_date.pop('id')

        for cell_action in obj['actions']:
            cell_action.pop('id')

        self.assertEqual(task['date'], obj['date'])
        self.assertEqual(task['text'], obj['text'])
        self.assertEqual(task['note'], obj['note'])
        self.assertEqual(task['dates'], obj['dates'])
        self.assertEqual(task['actions'], obj['actions'])
        self.assertEqual(task['lease_contract'], obj['lease_contract'])

    def test_reminder_nearest_date(self):
        reminder = {
            'date': '2023-10-01',
            'text': 'reminder 1',
            'dates': [{'date': (datetime.datetime.utcnow() + datetime.timedelta(days=3)).isoformat(), 'name': 'date_1'}, {'date': (datetime.datetime.utcnow() + datetime.timedelta(days=100)).isoformat(), 'name': 'date_2'}],
            'lease_contract': self.create_LeaseContract(),
        }
        success, obj = NotificationsApi.create_reminder(reminder)

        self.assertTrue(success)
        self.assertEqual(obj['nearest_date'], (datetime.datetime.utcnow() + datetime.timedelta(days=3)).strftime("%Y-%m-%d %H:%M"))

    def test_task_nearest_date(self):
        task = {
            'date': '2023-10-01',
            'text': 'task 1',
            'note': 'some Note',
            'dates': [{'date': (datetime.datetime.utcnow() + datetime.timedelta(days=3)).isoformat(), 'name': 'date_1'}, {'date': (datetime.datetime.utcnow() + datetime.timedelta(days=100)).isoformat(), 'name': 'date_2'}],
            'lease_contract': self.create_LeaseContract(),
        }
        success, obj = NotificationsApi.create_task(task)

        self.assertTrue(success)
        self.assertEqual(obj['nearest_date'], (datetime.datetime.utcnow() + datetime.timedelta(days=3)).strftime("%Y-%m-%d %H:%M"))

    def test_reminder_list_and_pagination(self):
        # settings.PAGINATION_PAGE_SIZE = 2
        reminder_1 = {
            'date': '2023-11-01',
            'text': 'reminder 1',
            'dates': [{'date': '2023-10-02T00:00:00', 'name': 'date_1'}, {'date': '2023-10-03T00:00:00', 'name': 'date_2'}],
            'lease_contract': self.create_LeaseContract(),
        }
        reminder_2 = {
            'date': '2023-11-02',
            'text': 'reminder 2',
            'dates': [{'date': '2023-10-02T00:00:00', 'name': 'date_1'}, {'date': '2023-10-03T00:00:00', 'name': 'date_2'}],
            'lease_contract': self.create_LeaseContract(),
        }
        reminder_3 = {
            'date': '2023-11-03',
            'text': 'reminder 3',
            'dates': [{'date': '2023-10-02T00:00:00', 'name': 'date_1'}, {'date': '2023-10-03T00:00:00', 'name': 'date_2'}],
            'lease_contract': self.create_LeaseContract(),
        }

        NotificationsApi.create_reminder(reminder_1)
        NotificationsApi.create_reminder(reminder_2)
        NotificationsApi.create_reminder(reminder_3)

        success, result1 = NotificationsApi.reminder_list()

        self.assertEqual(result1['previous'], None)
        self.assertEqual(type(result1['next']), str)
        
        success, result2 = NotificationsApi.reminder_list(final_url=result1['next'])

        self.assertEqual(type(result2['previous']), str)
        self.assertEqual(result2['next'], None)

        for named_date in result2['results'][0]['dates']:
            named_date.pop('id')

        self.assertEqual(result2['results'][0]['date'], reminder_3['date'])
        self.assertEqual(result2['results'][0]['text'], reminder_3['text'])
        self.assertEqual(result2['results'][0]['dates'], reminder_3['dates'])
        self.assertEqual(result2['results'][0]['lease_contract'], reminder_3['lease_contract'])

    def test_task_list_and_pagination(self):
        # settings.PAGINATION_PAGE_SIZE = 2
        task_1 = {
            'date': '2023-10-01',
            'text': 'task 1',
            'note': 'some Note',
            'dates': [{'date': '2023-10-02T00:00:00', 'name': 'date_1'}, {'date': '2023-10-03T00:00:00', 'name': 'date_2'}],
            'actions': [{'action': 'acton_1', 'done': False}],
            'lease_contract': self.create_LeaseContract(),
        }
        task_2 = {
            'date': '2023-10-01',
            'text': 'task 2',
            'note': 'some Note',
            'dates': [{'date': '2023-10-02T00:00:00', 'name': 'date_1'}, {'date': '2023-10-03T00:00:00', 'name': 'date_2'}],
            'actions': [{'action': 'acton_1', 'done': False}],
            'lease_contract': self.create_LeaseContract(),
        }
        task_3 = {
            'date': '2023-10-01',
            'text': 'task 3',
            'note': 'some Note',
            'dates': [{'date': '2023-10-02T00:00:00', 'name': 'date_1'}, {'date': '2023-10-03T00:00:00', 'name': 'date_2'}],
            'actions': [{'action': 'acton_1', 'done': False}],
            'lease_contract': self.create_LeaseContract(),
        }

        NotificationsApi.create_task(task_1)
        NotificationsApi.create_task(task_2)
        NotificationsApi.create_task(task_3)

        success, result1 = NotificationsApi.task_list()

        self.assertEqual(result1['previous'], None)
        self.assertEqual(type(result1['next']), str)
        
        success, result2 = NotificationsApi.task_list(final_url=result1['next'])

        self.assertEqual(type(result2['previous']), str)
        self.assertEqual(result2['next'], None)

        for named_date in result2['results'][0]['dates']:
            named_date.pop('id')

        for cell_action in result2['results'][0]['actions']:
            cell_action.pop('id')

        self.assertEqual(result2['results'][0]['date'], task_3['date'])
        self.assertEqual(result2['results'][0]['text'], task_3['text'])
        self.assertEqual(result2['results'][0]['dates'], task_3['dates'])
        self.assertEqual(result2['results'][0]['lease_contract'], task_3['lease_contract'])

    def test_get_non_existent_reminder(self):
        success, obj = NotificationsApi.get_reminder(1)
        self.assertFalse(success)

    def test_get_non_existent_task(self):
        success, obj = NotificationsApi.get_task(1)
        self.assertFalse(success)

    def test_update_remider(self):
        reminder = {
            'date': '2023-11-01',
            'text': 'reminder 1',
            'dates': [{'date': '2023-10-02T00:00:00', 'name': 'date_1'}, {'date': '2023-10-03T00:00:00', 'name': 'date_2'}],
            'lease_contract': self.create_LeaseContract(),
        }
        success, obj = NotificationsApi.create_reminder(reminder)

        reminder_new_data = {
            'id': obj['id'],
            'date': '2023-11-02',
            'text': 'reminder 2',
            'dates': [{'date': '2023-10-03T00:00:00', 'name': 'date_1'}, {'date': '2023-10-05T00:00:00', 'name': 'date_2'}],
        }

        success, obj = NotificationsApi.update_reminder(reminder_new_data)

        self.assertTrue(success)

        for named_date in obj['dates']:
            named_date.pop('id')

        self.assertEqual(reminder_new_data['date'], obj['date'])
        self.assertEqual(reminder_new_data['text'], obj['text'])
        self.assertEqual(reminder_new_data['dates'], obj['dates'])
        self.assertEqual(reminder['lease_contract'], obj['lease_contract'])

    def test_update_task(self):
        task = {
            'date': '2023-11-01',
            'text': 'task 1',
            'dates': [{'date': '2023-10-02T00:00:00', 'name': 'date_1'}, {'date': '2023-10-03T00:00:00', 'name': 'date_2'}],
            'lease_contract': self.create_LeaseContract(),
        }
        success, obj = NotificationsApi.create_task(task)

        task_new_data = {
            'id': obj['id'],
            'date': '2023-11-02',
            'text': 'reminder 2',
            'dates': [{'date': '2023-10-03T00:00:00', 'name': 'date_1'}, {'date': '2023-10-05T00:00:00', 'name': 'date_2'}],
        }

        success, obj = NotificationsApi.update_task(task_new_data)

        self.assertTrue(success)

        for named_date in obj['dates']:
            named_date.pop('id')

        self.assertEqual(task_new_data['date'], obj['date'])
        self.assertEqual(task_new_data['text'], obj['text'])
        self.assertEqual(task_new_data['dates'], obj['dates'])
        self.assertEqual(task['lease_contract'], obj['lease_contract'])

    def test_filter_reminder_list(self):
        reminder_1 = {
            'date': '2023-11-01',
            'text': 'reminder 1',
            'dates': [{'date': '2023-10-02T00:00:00', 'name': 'date_1'}, {'date': '2023-10-03T00:00:00', 'name': 'date_2'}],
            'lease_contract': self.create_LeaseContract(),
        }
        reminder_2 = {
            'date': '2023-11-02',
            'text': 'reminder 2',
            'dates': [{'date': '2023-10-02T00:00:00', 'name': 'date_1'}, {'date': '2023-10-03T00:00:00', 'name': 'date_2'}],
            'lease_contract': self.create_LeaseContract(),
        }
        reminder_3 = {
            'date': '2023-11-03',
            'text': 'reminder 3',
            'dates': [{'date': '2023-10-02T00:00:00', 'name': 'date_1'}, {'date': '2023-10-03T00:00:00', 'name': 'date_2'}],
            'lease_contract': self.create_LeaseContract(),
        }

        NotificationsApi.create_reminder(reminder_1)
        NotificationsApi.create_reminder(reminder_2)
        NotificationsApi.create_reminder(reminder_3)

        success, result = NotificationsApi.reminder_list(reminder_3['lease_contract']['tenant']['email'])

        self.assertEqual(len(result['results']), 1)
        self.assertEqual(result['previous'], None)
        self.assertEqual(result['next'], None)

        for named_date in result['results'][0]['dates']:
            named_date.pop('id')

        self.assertEqual(result['results'][0]['date'], reminder_3['date'])
        self.assertEqual(result['results'][0]['text'], reminder_3['text'])
        self.assertEqual(result['results'][0]['dates'], reminder_3['dates'])
        self.assertEqual(result['results'][0]['lease_contract'], reminder_3['lease_contract'])

    def test_filter_task_list(self):
        task_1 = {
            'date': '2023-11-01',
            'text': 'reminder 1',
            'dates': [{'date': '2023-10-02T00:00:00', 'name': 'date_1'}, {'date': '2023-10-03T00:00:00', 'name': 'date_2'}],
            'lease_contract': self.create_LeaseContract(),
        }
        task_2 = {
            'date': '2023-11-02',
            'text': 'reminder 2',
            'dates': [{'date': '2023-10-02T00:00:00', 'name': 'date_1'}, {'date': '2023-10-03T00:00:00', 'name': 'date_2'}],
            'lease_contract': self.create_LeaseContract(),
        }
        task_3 = {
            'date': '2023-11-03',
            'text': 'reminder 3',
            'dates': [{'date': '2023-10-02T00:00:00', 'name': 'date_1'}, {'date': '2023-10-03T00:00:00', 'name': 'date_2'}],
            'lease_contract': self.create_LeaseContract(),
        }

        NotificationsApi.create_task(task_1)
        NotificationsApi.create_task(task_2)
        NotificationsApi.create_task(task_3)

        success, result = NotificationsApi.task_list(task_3['lease_contract']['tenant']['email'])

        self.assertEqual(len(result['results']), 1)
        self.assertEqual(result['previous'], None)
        self.assertEqual(result['next'], None)

        for named_date in result['results'][0]['dates']:
            named_date.pop('id')

        self.assertEqual(result['results'][0]['date'], task_3['date'])
        self.assertEqual(result['results'][0]['text'], task_3['text'])
        self.assertEqual(result['results'][0]['dates'], task_3['dates'])
        self.assertEqual(result['results'][0]['lease_contract'], task_3['lease_contract'])

    def test_filter_reminder_list_by_active(self):
        reminder_1 = {
            'date': '2023-11-01',
            'text': 'reminder 1',
            'dates': [{'date': (datetime.datetime.utcnow() + datetime.timedelta(days=3)).isoformat(), 'name': 'date_1'}, {'date': '2023-10-03T00:00:00', 'name': 'date_2'}],
            'lease_contract': self.create_LeaseContract(),
        }
        reminder_2 = {
            'date': '2023-11-02',
            'text': 'reminder 2',
            'dates': [{'date': '2023-10-02T00:00:00', 'name': 'date_1'}, {'date': '2023-10-03T00:00:00', 'name': 'date_2'}],
            'lease_contract': self.create_LeaseContract(),
        }
        reminder_3 = {
            'date': '2023-11-03',
            'text': 'reminder 3',
            'dates': [{'date': '2023-10-02T00:00:00', 'name': 'date_1'}, {'date': '2023-10-03T00:00:00', 'name': 'date_2'}],
            'lease_contract': self.create_LeaseContract(),
        }

        NotificationsApi.create_reminder(reminder_1)
        NotificationsApi.create_reminder(reminder_2)
        NotificationsApi.create_reminder(reminder_3)

        success, result = NotificationsApi.reminder_list(active=True)

        self.assertEqual(len(result['results']), 1)
        self.assertEqual(result['previous'], None)
        self.assertEqual(result['next'], None)

        for named_date in result['results'][0]['dates']:
            named_date.pop('id')

        self.assertEqual(result['results'][0]['date'], reminder_1['date'])
        self.assertEqual(result['results'][0]['text'], reminder_1['text'])
        self.assertEqual(result['results'][0]['dates'], reminder_1['dates'])
        self.assertEqual(result['results'][0]['lease_contract'], reminder_1['lease_contract'])

    def test_filter_task_list_by_active(self):
        task_1 = {
            'date': '2023-11-01',
            'text': 'reminder 1',
            'dates': [{'date': (datetime.datetime.utcnow() + datetime.timedelta(days=3)).isoformat(), 'name': 'date_1'}, {'date': '2023-10-03T00:00:00', 'name': 'date_2'}],
            'lease_contract': self.create_LeaseContract(),
        }
        task_2 = {
            'date': '2023-11-02',
            'text': 'reminder 2',
            'dates': [{'date': '2023-10-02T00:00:00', 'name': 'date_1'}, {'date': '2023-10-03T00:00:00', 'name': 'date_2'}],
            'lease_contract': self.create_LeaseContract(),
        }
        task_3 = {
            'date': '2023-11-03',
            'text': 'reminder 3',
            'dates': [{'date': '2023-10-02T00:00:00', 'name': 'date_1'}, {'date': '2023-10-03T00:00:00', 'name': 'date_2'}],
            'lease_contract': self.create_LeaseContract(),
        }

        NotificationsApi.create_task(task_1)
        NotificationsApi.create_task(task_2)
        NotificationsApi.create_task(task_3)

        success, result = NotificationsApi.task_list(active=True)

        self.assertEqual(len(result['results']), 1)
        self.assertEqual(result['previous'], None)
        self.assertEqual(result['next'], None)

        for named_date in result['results'][0]['dates']:
            named_date.pop('id')

        self.assertEqual(result['results'][0]['date'], task_1['date'])
        self.assertEqual(result['results'][0]['text'], task_1['text'])
        self.assertEqual(result['results'][0]['dates'], task_1['dates'])
        self.assertEqual(result['results'][0]['lease_contract'], task_1['lease_contract'])

def clear_db():
    ReminderNamedDate = Reminder.dates.get_through_model()
    TaskNamedDate = Task.dates.get_through_model()
    TaskCellAction = Task.actions.get_through_model()
    Tenant.delete().execute()
    Owner.delete().execute()
    Apartment.delete().execute()
    LeaseContract.delete().execute()
    UtilityBills.delete().execute()
    Transaction.delete().execute()
    NamedDate.delete().execute()
    CellAction.delete().execute()
    Reminder.delete().execute()
    Task.delete().execute()
    ReminderNamedDate.delete().execute()
    TaskNamedDate.delete().execute()
    TaskCellAction.delete().execute()

if __name__ == '__main__':
    clear_db()
    settings.PAGINATION_PAGE_SIZE = 2
    create_tables()
    unittest.main()
    clear_db()

# TenantApi +
# OwnerApi +
# ApartmentApi +
# TransactionApi +
# LeaseContractApi +
# NotificationsApi +
