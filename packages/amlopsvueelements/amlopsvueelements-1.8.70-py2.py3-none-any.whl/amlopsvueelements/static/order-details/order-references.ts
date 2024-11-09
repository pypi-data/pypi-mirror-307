import Api from '@/services';
import { getIsAdmin } from '@/helpers';
import type { AddCRMActivityRequest, DeleteCRMActivityRequest } from '../mutations/crm-activity';

import type {
  IAircraft,
  IAircraftLocations,
  IAircraftTypeEntity,
  IAirport,
  IAirportLocations,
  IClient,
  IConversation,
  ICreditExposure,
  ICrmActivity,
  ICrmActivityType,
  IFuelUnit,
  IGroundHandler,
  IOperator,
  IOrder,
  IOrderPerson,
  IOrderRoi,
  IOrderStatus,
  IOrderType,
  IOrganisation,
  IPaginatedResponse,
  IRecentFlightsResponse,
  IService,
  ITypeReference
} from 'shared/types';
import type { ISupplierFuelDetails } from 'shared/types';
import type { IActivity, IFuelPricingObj, IProceedCompliance, ISupplierFuel } from 'shared/types';

class OrderReferenceService extends Api {
  async fetchOrderStatuses() {
    const { data } = await this.get<IOrderStatus[]>(`api/v1/orders/order_statuses/?search=`);
    return data && typeof data === 'object' ? data : [];
  }

  async fetchOrderTypes() {
    const { data } = await this.get<IOrderType[]>(`api/v1/orders/order_types/`);
    return data;
  }

  async fetchOrganisations(search?: string) {
    const {
      data: { results: organisations }
    } = await this.get<IPaginatedResponse<IOrganisation[]>>('api/v1/admin/organisations/', {
      params: { search, 'page[size]': 999 }
    });
    return organisations;
  }

  async fetchOrganisationPeople(organisationId: number) {
    if (!organisationId) return [];
    const url = `api/v1/organisations/${organisationId}/people/`;
    const { data } = await this.get<IOrderPerson[]>(url);
    return data.map((item) => ({
      ...item,
      display: `${item.details.full_name} (${item.jobs[0]?.job_title})`,
      display_email: `${item.details.full_name} ${item.details.contact_email}`
    }));
  }

  async fetchAircraftTypes(organisationId: number) {
    if (getIsAdmin() && !organisationId) return [];
    const url = getIsAdmin()
      ? `api/v1/admin/organisation/${organisationId}/aircraft_types/`
      : `api/v1/organisation/aircraft_types/`;
    const {
      data: { data }
    } = await this.get<{ data: IAircraftTypeEntity[] }>(url);
    return data.map((el) => ({
      ...el,
      full_repr: `${el.attributes.manufacturer} ${el.attributes.model} (${el.attributes.designator})`
    }));
  }

  async fetchAircrafts(organisationId: number) {
    if (!organisationId) return [];
    const url = `api/v1/aircraft/`;
    const { data } = await this.get<IAircraft[]>(url, {
      params: { operator: organisationId }
    });
    return data;
  }

  async fetchAirportLocations(search?: string | number) {
    const {
      data: { results: airports }
    } = await this.get<IPaginatedResponse<IAirport[]>>('api/v1/organisations/', {
      params: {
        search,
        type: 8,
        optional_fields: 'country'
      }
    });
    return airports;
  }

  async fetchFuelQuantityUnits() {
    const { data } = await this.get<IFuelUnit[]>('api/v1/uom/');
    return data;
  }

  async fetchFuelCategories() {
    const { data } = await this.get<ITypeReference[]>('api/v1/fuel_categories/');
    return data;
  }

  async fetchGroundHandlers(airportId: number) {
    const {
      data: { results: handlers }
    } = await this.get<IPaginatedResponse<IGroundHandler[]>>('api/v1/organisations/', {
      params: {
        type: 3,
        gh_location: airportId
      }
    });
    return handlers;
  }

  async fetchClients() {
    const {
      data: { results: clients }
    } = await this.get<IPaginatedResponse<IClient[]>>('api/v1/organisations/', {
      params: {
        type_str: 'client',
        optional_fields: 'client_status_list'
      }
    });
    return clients;
  }

  async fetchOperators() {
    const {
      data: { results: operators }
    } = await this.get<IPaginatedResponse<IOperator[]>>('api/v1/organisations/', {
      params: {
        type_str: 'operator'
      }
    });
    return operators;
  }

  async fetchMissionTypes() {
    const { data } = await this.get<ITypeReference[]>('api/v1/admin/handling_requests/types/');
    return data;
  }

  async fetchPersonTitles() {
    const { data } = await this.get<ITypeReference[]>('api/v1/person_titles/');
    return data;
  }

  async fetchPersonRoles() {
    const { data } = await this.get<ITypeReference[]>('api/v1/person_roles/');
    return data;
  }

  async fetchServices(
    locationId?: string | number,
    organisationId?: string | number,
    codeName?: string
  ) {
    const { data } = await this.get<{ data: IService[] }>('api/v1/handling_services/', {
      params: { organisation_id: organisationId, location_id: locationId, codename: codeName }
    });
    return data.data
      ?.filter((service) => {
        return !(
          service.attributes.is_dla &&
          !service.attributes.is_dla_visible_arrival &&
          !service.attributes.is_dla_visible_departure
        );
      })
      .map((service) => ({
        ...service,
        id: Number(service.id)
      }));
  }

  async fetchMeta() {
    const { data } = await this.get('api/v1/meta/');
    return data;
  }

  async fetchSupplierFuel(
    orderPricingCalculationRecord: IOrder['pricing_calculation_record']
  ): Promise<ISupplierFuel | null> {
    const { data } = await this.get<ISupplierFuel>(
      `api/v1/pricing/supplier_fuel_pricing/${orderPricingCalculationRecord}/`
    );
    return typeof data === 'object' ? data : null;
  }

  async fetchSupplierFuelDetails({
    supplierId,
    detailsId
  }: {
    supplierId: number;
    detailsId: number;
  }): Promise<ISupplierFuelDetails> {
    const { data } = await this.get<ISupplierFuelDetails>(
      `api/v1/pricing/supplier_fuel_pricing/${supplierId}/results/${detailsId}/`
    );
    return data;
  }

  async selectFuelSupplier(orderId: number, payload: any) {
    const { data } = await this.post<any[]>(
      `api/v1/orders/${orderId}/fuel_pricing/from_pricing_record/`,
      payload
    );
    return data;
  }

  async fetchOrderPricing(orderId: number): Promise<IFuelPricingObj> {
    const { data } = await this.get<IFuelPricingObj>(`api/v1/orders/${orderId}/fuel_pricing/`);
    return data;
  }

  async updateOrderPricing(orderId: number, payload: any): Promise<IFuelPricingObj> {
    const { data } = await this.put<IFuelPricingObj>(
      `api/v1/orders/${orderId}/fuel_pricing/`,
      payload
    );
    return data;
  }

  async updateOrderROI(orderId: number, payload: any) {
    const { data } = await this.post<IOrderRoi>(`api/v1/orders/${orderId}/roi/`, payload);
    return data;
  }

  async fetchFlightAirportLocations(id: number): Promise<IAirportLocations> {
    const { data } = await this.post<any>(`api/v1/sfr_tracking/airport_locations/`, {
      handling_request: id.toString()
    });
    return data;
  }

  async fetchFlightAircraftLocations(id: number): Promise<IAircraftLocations> {
    const { data } = await this.post<any>(`api/v1/sfr_tracking/aircraft_locations/`, {
      handling_request: id.toString()
    });
    return data;
  }

  async fetchOrderQuoteButton(orderId: number) {
    const { data } = await this.get<any>(`api/v1/orders/${orderId}/quote_button/`);
    return data;
  }

  async fetchRecentFlights(orderId: number) {
    const { data } = await this.get<IRecentFlightsResponse>(
      `api/v1/orders/${orderId}/recent_flights/`
    );
    return typeof data === 'object' ? data : null;
  }

  async fetchHandlingServices() {
    const { data } = await this.get<any>(`api/v1/handling_services/`);
    return typeof data === 'object' ? data : null;
  }

  async fetchActivityLog(orderId: number) {
    const { data } = await this.get<IActivity[]>(`api/v1/orders/${orderId}/activity_log/`);
    return data;
  }

  async fetchCreditExposure(orderId: number) {
    const { data } = await this.get<ICreditExposure>(`api/v1/orders/${orderId}/credit_exposure/`);
    return data;
  }

  async fetchProceedCompliance(orderId: number) {
    const { data } = await this.get<IProceedCompliance>(
      `api/v1/orders/${orderId}/proceed_to_compliance/`
    );
    return data;
  }

  async fetchRequestManagementApproval(orderId: number) {
    const { data } = await this.get<{
      detail: string;
    }>(`api/v1/orders/${orderId}/request_management_approval/`);
    return data;
  }

  async fetchOrderConversation(id: number): Promise<IConversation> {
    const { data } = await this.post<IConversation>(
      `api/v1/orders/${id}/create_staff_conversation/`
    );
    return data;
  }

  async fetchOrderCRM(orderId: number) {
    const { data } = await this.get<ICrmActivity[]>(`api/v1/orders/${orderId}/crm_activity/`);
    return data;
  }

  async fetchOrderCRMTypes() {
    const { data } = await this.get<ICrmActivityType[]>(`api/v1/crm_activity_types/`);
    return data;
  }

  async addCRMActivity(request: AddCRMActivityRequest) {
    const { orderId, payload } = request;
    const { data } = await this.post<ICrmActivity>(
      `api/v1/orders/${orderId}/crm_activity/`,
      payload
    );
    return data;
  }

  async deleteCRMActivity(request: DeleteCRMActivityRequest) {
    const { orderId, activityId } = request;
    const { data } = await this.delete<ICrmActivity>(
      `api/v1/orders/${orderId}/crm_activity/${activityId}/`
    );
    return data;
  }

  async updateCRMActivity(request: AddCRMActivityRequest) {
    const { orderId, payload } = request;
    const { data } = await this.patch<ICrmActivity>(
      `api/v1/orders/${orderId}/crm_activity/`,
      payload
    );
    return data;
  }
}

export default new OrderReferenceService();
