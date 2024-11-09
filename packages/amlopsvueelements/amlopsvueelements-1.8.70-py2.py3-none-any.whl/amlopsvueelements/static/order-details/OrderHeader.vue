<template>
  <div ref="header" class="order-header flex flex-col">
    <SendViaEmailModal
      ref="emailInput"
      :is-open="isEmailModalOpened"
      :organisation-id="order?.client?.id"
      name="email-modal"
      @modal-close="isEmailModalOpened = false"
      @modal-submit.prevent=""
    />
    <SendSupplierOrderRequestModal
      ref="supplierInput"
      :is-open="isSupplierOrderRequestModalOpened"
      :organisation-id="order?.client?.id"
      name="supplier-modal"
      @modal-close="isSupplierOrderRequestModalOpened = false"
      @modal-submit.prevent=""
    />
    <SendClientFuelReleaseModal
      ref="clientInput"
      :is-open="isClientFuelReleaseModalOpened"
      :organisation-id="order?.client?.id"
      name="client-modal"
      @modal-close="isClientFuelReleaseModalOpened = false"
      @modal-submit.prevent=""
    />
    <MarkNoUpliftModal
      ref="markInput"
      :is-open="isMarkNoUpliftModalOpened"
      :organisation-id="order?.client?.id"
      name="mark-modal"
      @modal-close="isMarkNoUpliftModalOpened = false"
      @modal-submit.prevent=""
    />
    <ConfirmSupplierOrderModal
      ref="markInput"
      :is-open="isConfirmSupplierOrderModalOpened"
      :organisation-id="order?.client?.id"
      name="confirm-modal"
      @modal-close="isConfirmSupplierOrderModalOpened = false"
      @modal-submit.prevent=""
    />
    <SubmitDeliveryTicketDetailsModal
      ref="markInput"
      :is-open="isSubmitDeliveryTicketDetailsModalOpened"
      :organisation-id="order?.client?.id"
      name="confirm-modal"
      @modal-close="isSubmitDeliveryTicketDetailsModalOpened = false"
      @modal-submit.prevent=""
    />
    <div
      class="order-status flex w-full justify-between items-center mb-4 px-[1rem] pt-[0.5rem] pb-[0.6rem]"
      :style="{
        // eslint-disable-next-line prettier/prettier
        background: `repeating-linear-gradient(50deg,${changeColorAlpha(getColor(), 0.05)},${changeColorAlpha(getColor(), 0.05)} 10px,rgb(255, 255, 255) 0,rgb(255, 255, 255) 20px)`, 
        color: getTextColor(),
        'border-top': `4px solid ${getColor()}`,
        'border-bottom': `1px solid ${changeColorAlpha(getColor(), 0.2)}`
      }"
    >
      <div class="status flex py-[0.25rem]" :style="{ color: getColor() }">
        <span>{{ order?.status?.status_name?.toUpperCase() }}</span>
      </div>
      <div v-if="currentStep === 1" class="status-buttons flex gap-3">
        <ButtonPopover v-show="true || quoteButton?.state === 'active'">
          <template #default>
            <div class="button">{{ quoteButton?.button_text ?? 'Send Client Quote' }}</div>
          </template>
          <template #popup>
            <div class="send-via-email-popup flex gap-2 cursor-pointer">
              <div class="el flex gap-2" @click="isEmailModalOpened = true">
                <img width="20" height="20" src="../../assets/icons/mail.svg" alt="email" />
                Send via email
              </div>
            </div>
          </template>
        </ButtonPopover>
        <Button class="button button-green flex items-center gap-2" @click="onProceedToCompliance">
          Proceed to Compliance
        </Button>
      </div>
      <div v-if="currentStep === 2" class="status-buttons flex gap-3">
        <Button class="button"> Proceed to Order </Button>
        <Button class="button cancel-button items-center gap-2">
          <img width="12" height="12" src="../../assets/icons/cross.svg" alt="delete" />
          Decline Order
        </Button>
        <Button class="button button-green flex items-center gap-2">
          <img src="../../assets/icons/check.svg" alt="approve" />
          Approve Order
        </Button>
      </div>
      <div v-if="currentStep === 3" class="status-buttons flex gap-3">
        <ButtonPopover :left="true">
          <template #default>
            <div class="button">
              Send
              <img width="20" height="20" src="../../assets/icons/chevron-down.svg" alt="delete" />
            </div>
          </template>
          <template #popup>
            <div class="send-via-email-popup flex flex-col gap-2 cursor-pointer">
              <div class="el flex gap-2" @click="isEmailModalOpened = true">
                <img width="20" height="20" src="../../assets/icons/gas.svg" alt="gas" />
                Send via Email
              </div>
              <div class="el flex gap-2" @click="isSupplierOrderRequestModalOpened = true">
                <img width="20" height="20" src="../../assets/icons/gas.svg" alt="gas" />
                Send Supplier Order Request
              </div>
              <div class="el flex gap-2" @click="isClientFuelReleaseModalOpened = true">
                <img width="20" height="20" src="../../assets/icons/gas.svg" alt="gas" />
                Send Client Fuel Release
              </div>
              <div class="el flex gap-2" @click="isMarkNoUpliftModalOpened = true">
                <img width="20" height="20" src="../../assets/icons/gas.svg" alt="gas" />
                Mark as No-Uplift
              </div>
              <div class="el flex gap-2" @click="isConfirmSupplierOrderModalOpened = true">
                <img width="20" height="20" src="../../assets/icons/gas.svg" alt="gas" />
                Confirm Supplier Order
              </div>
              <div class="el flex gap-2" @click="isSubmitDeliveryTicketDetailsModalOpened = true">
                <img width="20" height="20" src="../../assets/icons/gas.svg" alt="gas" />
                Submit Delivery Ticket Details
              </div>
            </div>
          </template>
        </ButtonPopover>
        <Button class="button"> Submit Delivery Ticket Details </Button>
        <Button class="button cancel-button items-center gap-2">
          <img width="12" height="12" src="../../assets/icons/cross.svg" alt="delete" />
          Mark as No-Uplift
        </Button>
        <Button class="button button-green flex items-center gap-2">
          <img src="../../assets/icons/check.svg" alt="approve" />
          Confirm Supplier Order
        </Button>
      </div>
    </div>
    <div class="order-name-wrap mb-4 px-[1rem] flex flex-col">
      <div class="order-name-row flex gap-2 items-center">
        <div class="order-name">
          {{ order?.aml_order_number }}
        </div>
        <div
          v-if="order?.linked_order"
          class="order-linked flex items-center px-[0.5rem] gap-2 cursor-pointer"
          @click="redirectToLinkedOrder(order?.linked_order?.uri!)"
        >
          <img src="../../assets/icons/linked.svg" alt="linked" />
          <div class="order-linked-text">
            {{ order?.linked_order?.aml_order_number }}
          </div>
        </div>
        <Avatar
          v-if="order?.assigned_aml_person"
          :first-name="order?.assigned_aml_person?.details?.first_name"
          :last-name="order?.assigned_aml_person?.details?.last_name"
          :is-small="true"
        ></Avatar>
      </div>
      <div
        class="order-company cursor-pointer flex w-fit"
        @click="redirectToURL(order?.client?.url)"
      >
        {{ order?.client?.details?.registered_name }}
        <img
          width="12"
          height="12"
          src="../../assets/icons/chevron-right.svg"
          alt="warn"
          class="warn ml-[0.25rem]"
        />
      </div>
    </div>
    <div v-if="order?.type?.is_fuel" class="order-content flex pb-[1rem] px-[1rem] gap-2">
      <div class="order-content-col w-4/12 flex flex-col gap-1.5">
        <div
          v-if="!order?.fuel_order?.is_open_release"
          class="order-content-el flex gap-3 items-start"
        >
          <div class="order-content-header w-4/12">Uplift Time (UTC)</div>
          <div class="order-content-data w-8/12">
            {{
              order?.fulfilment_datetime
                ? order?.fulfilment_time_tbc
                  ? order?.fulfilment_datetime_str + ' (Time TBC)'
                  : order?.fulfilment_datetime_str
                : 'TBC'
            }}
          </div>
        </div>
        <div v-else class="order-content-el flex gap-3 items-start">
          <div class="order-content-header w-4/12">Release Start Date</div>
          <div class="order-content-data w-8/12">
            {{
              order?.fuel_order?.arrival_time_tbc
                ? order?.fuel_order?.arrival_datetime_utc
                : order?.fuel_order?.arrival_datetime_utc.slice(0, 10)
            }}
          </div>
        </div>
        <div class="order-content-el flex gap-3 items-start">
          <div class="order-content-header w-4/12">IPA</div>
          <div class="order-content-data w-8/12">
            <span
              :class="{ 'cursor-pointer': order?.fuel_order?.ipa }"
              @click="redirectToURL(order?.fuel_order?.ipa?.url)"
            ></span>
            {{ order?.fuel_order?.ipa?.full_repr ?? 'TBC' }}
            <img
              v-if="order?.fuel_order?.ipa"
              width="12"
              height="12"
              src="../../assets/icons/chevron-right.svg"
              alt="warn"
              class="warn cursor-pointer ml-[0.25rem]"
              @click="redirectToURL(order?.fuel_order?.ipa?.url)"
            />
          </div>
        </div>
        <div class="order-content-el flex gap-3 items-start">
          <div class="order-content-header w-4/12">Operator</div>
          <div class="order-content-data w-8/12">
            <span class="cursor-pointer" @click="redirectToURL(order?.operator?.url)">
              {{ order?.operator?.details?.registered_name }}</span
            >
            <img
              width="12"
              height="12"
              src="../../assets/icons/chevron-right.svg"
              alt="warn"
              class="warn cursor-pointer ml-[0.25rem]"
              @click="redirectToURL(order?.operator?.url)"
            />
          </div>
        </div>
        <div class="order-content-el flex gap-3 items-start">
          <div class="order-content-header w-4/12">Location</div>
          <div class="order-content-data w-8/12">
            <span class="cursor-pointer" @click="redirectToURL(order?.location?.url)">
              {{ order?.location?.full_repr }}</span
            >
            <img
              width="12"
              height="12"
              src="../../assets/icons/chevron-right.svg"
              alt="warn"
              class="warn cursor-pointer ml-[0.25rem]"
              @click="redirectToURL(order?.location?.url)"
            />
          </div>
        </div>
        <div v-if="order?.sfr" class="order-content-el flex gap-3 items-start">
          <div class="order-content-header w-4/12 cursor-pointer">S&F Request</div>
          <div
            class="order-content-data w-8/12 flex items-center gap-1 cursor-pointer"
            @click="redirectToURL(order?.sfr?.url)"
          >
            <div
              class="status px-[0.5rem] py-[0.25rem] border-0 rounded-md"
              :style="{
                'background-color':
                  order?.sfr?.sfr_status?.background_color ?? 'rgb(255, 255, 255)',
                color: order?.sfr?.sfr_status?.text_color
              }"
            >
              {{ order?.sfr?.reference }}
            </div>
          </div>
        </div>
      </div>
      <div class="order-content-col w-4/12 flex flex-col gap-1.5">
        <div
          v-if="!order?.fuel_order?.is_open_release"
          class="order-content-el flex gap-3 items-start"
        >
          <div class="order-content-header w-5/12">Uplift Time (Local)</div>
          <div class="order-content-data w-7/12">
            {{
              order?.fulfilment_datetime
                ? order?.fulfilment_time_tbc
                  ? order?.fulfilment_datetime_str + ' (Time TBC)'
                  : toLocalTime(order?.fulfilment_datetime)
                : 'TBC'
            }}
          </div>
        </div>
        <div v-else class="order-content-el flex gap-3 items-start">
          <div class="order-content-header w-5/12">Release End Date</div>
          <div class="order-content-data w-7/12">
            {{
              order?.fuel_order?.departure_time_tbc
                ? order?.fuel_order?.departure_datetime_utc
                : order?.fuel_order?.deaprture_datetime_utc.slice(0, 10)
            }}
          </div>
        </div>
        <div class="order-content-el flex gap-3 items-start">
          <div class="order-content-header w-5/12">Fuel</div>
          <div v-if="!order?.fuel_order?.is_open_release" class="order-content-data w-7/12">
            {{
              `${order?.fuel_order?.fuel_category?.name}, ${addThousandSeparators(
                order?.fuel_order?.fuel_quantity
              )}
            ${order?.fuel_order?.fuel_uom?.description_plural}`
            }}
          </div>
          <div v-else class="order-content-data w-7/12 relative">
            {{ `${order?.fuel_order?.fuel_category?.name}` }}
            <div class="hover-wrap contents">
              <img
                width="16"
                height="16"
                src="../../assets/icons/info-circle.svg"
                alt="warn"
                class="warn"
              />
              <div class="order-content-data-tooltip">
                An indicative fuel quantity of
                {{ addThousandSeparators(order?.fuel_order?.fuel_quantity) }}
                {{ order?.fuel_order?.fuel_uom?.description_plural }} has been used for the purposes
                of calculating the order value and ROI
              </div>
            </div>
          </div>
        </div>
        <div class="order-content-el flex gap-3 items-start">
          <div class="order-content-header w-5/12">Supplier</div>
          <div class="order-content-data w-7/12">
            <span
              :class="{ 'cursor-pointer': order?.fuel_order?.supplier }"
              @click="redirectToURL(order?.fuel_order?.supplier?.url)"
              >{{ order?.fuel_order?.supplier?.details?.registered_name ?? 'TBC' }}</span
            >
            <img
              v-if="order?.fuel_order?.supplier"
              width="12"
              height="12"
              src="../../assets/icons/chevron-right.svg"
              alt="warn"
              class="warn cursor-pointer ml-[0.25rem]"
              @click="redirectToURL(order?.fuel_order?.supplier?.url)"
            />
          </div>
        </div>
        <div class="order-content-el flex gap-3 items-start">
          <div class="order-content-header w-5/12">Callsign</div>
          <div class="order-content-data w-7/12">
            {{ order?.callsign }}
          </div>
        </div>
      </div>
      <div class="order-content-col w-4/12 flex flex-col gap-1.5">
        <div class="order-content-el flex gap-3 items-start">
          <div class="order-content-header w-4/12">Handler</div>
          <div class="order-content-data w-8/12">
            <span
              :class="{ 'cursor-pointer': order?.fuel_order?.ground_handler }"
              @click="redirectToURL(order?.fuel_order?.ground_handler?.url)"
              >{{ order?.fuel_order?.ground_handler?.details?.registered_name ?? 'TBC' }}</span
            >
            <img
              v-if="order?.fuel_order?.ground_handler"
              width="12"
              height="12"
              src="../../assets/icons/chevron-right.svg"
              alt="warn"
              class="warn cursor-pointer ml-[0.25rem]"
              @click="redirectToURL(order?.fuel_order?.ground_handler?.url)"
            />
          </div>
        </div>
        <div class="order-content-el flex gap-3 items-start">
          <div class="order-content-header w-4/12">Aircraft</div>
          <div v-if="order?.is_any_aircraft" class="order-content-data w-8/12">Any aircraft</div>
          <div v-else-if="order?.tails.length > 0" class="order-content-data w-8/12 flex flex-col">
            <div v-for="aircraft in order?.tails" :key="aircraft.id">
              {{ aircraft?.tail_number?.full_repr ?? 'Aircraft' }}
            </div>
          </div>
          <div
            v-else-if="order?.tails.length === 0 && order?.aircraft_type"
            class="order-content-data w-8/12"
          >
            {{ order?.aircraft_type?.full_repr }}
          </div>
        </div>
      </div>
    </div>
    <div v-if="order?.type?.is_gh" class="order-content flex pb-[1rem] px-[1rem] gap-2">
      <div class="order-content-col w-5/12">
        <div class="order-content-el flex gap-3 items-start">
          <div class="order-content-header w-4/12">Callsign</div>
          <div class="order-content-data w-8/12">
            {{ order?.callsign }}
          </div>
        </div>
        <div class="order-content-el flex gap-3 items-start">
          <div class="order-content-header w-4/12">ETA (UTC)</div>
          <div class="order-content-data w-8/12">
            {{
              order?.gh_order?.arrival_time_tbc
                ? order?.gh_order?.arrival_datetime_utc + ' (Time TBC)'
                : order?.gh_order?.arrival_datetime_utc
            }}
          </div>
        </div>
        <div class="order-content-el flex gap-3 items-start">
          <div class="order-content-header w-4/12">ETA (Local)</div>
          <div class="order-content-data w-8/12">
            {{
              order?.gh_order?.arrival_time_tbc
                ? order?.gh_order?.arrival_datetime_utc + ' (Time TBC)'
                : toLocalTime(order?.gh_order?.arrival_datetime_utc!)
            }}
          </div>
        </div>
        <div class="order-content-el flex gap-3 items-start">
          <div class="order-content-header w-4/12">Location</div>
          <div class="order-content-data w-8/12">
            <span class="cursor-pointer" @click="redirectToURL(order?.location?.url)">
              {{ order?.location?.full_repr }}</span
            >
            <img
              width="12"
              height="12"
              src="../../assets/icons/chevron-right.svg"
              alt="warn"
              class="warn cursor-pointer ml-[0.25rem]"
              @click="redirectToURL(order?.location?.url)"
            />
          </div>
        </div>
        <div class="order-content-el flex gap-3 items-start">
          <div class="order-content-header w-4/12">Operator</div>
          <div class="order-content-data w-8/12">
            <span class="cursor-pointer" @click="redirectToURL(order?.operator?.url)">
              {{ order?.operator?.details?.registered_name }}</span
            >
            <img
              width="12"
              height="12"
              src="../../assets/icons/chevron-right.svg"
              alt="warn"
              class="warn cursor-pointer ml-[0.25rem]"
              @click="redirectToURL(order?.operator?.url)"
            />
          </div>
        </div>
      </div>
      <div class="order-content-col w-5/12">
        <div class="order-content-el flex gap-3 items-start">
          <div class="order-content-header w-4/12">Aircraft</div>
          <div v-if="order?.is_any_aircraft" class="order-content-data w-8/12">Any aircraft</div>
          <div v-else-if="order?.tails.length > 0" class="order-content-data w-8/12 flex flex-col">
            <div v-for="aircraft in order?.tails" :key="aircraft.id">
              {{ aircraft?.tail_number?.full_repr ?? 'Aircraft' }}
            </div>
          </div>
          <div
            v-else-if="order?.tails.length === 0 && order?.aircraft_type"
            class="order-content-data w-8/12"
          >
            {{ order?.aircraft_type?.full_repr }}
          </div>
        </div>
        <div class="order-content-el flex gap-3 items-start">
          <div class="order-content-header w-4/12">ETD (UTC)</div>
          <div class="order-content-data w-8/12">
            {{
              order?.gh_order?.departure_time_tbc
                ? order?.gh_order?.departure_datetime_utc + ' (Time TBC)'
                : order?.gh_order?.departure_datetime_utc
            }}
          </div>
        </div>
        <div class="order-content-el flex gap-3 items-start">
          <div class="order-content-header w-4/12">ETD (Local)</div>
          <div class="order-content-data w-8/12">
            {{
              order?.gh_order?.departure_time_tbc
                ? order?.gh_order?.departure_datetime_utc + ' (Time TBC)'
                : toLocalTime(order?.gh_order?.departure_datetime_utc!)
            }}
          </div>
        </div>
        <div class="order-content-el flex gap-3 items-start">
          <div class="order-content-header w-4/12">Supplier</div>
          <div class="order-content-data w-8/12">
            {{ order?.gh_order?.ground_handler?.details?.registered_name ?? 'TBC' }}
          </div>
        </div>
        <div v-if="order?.sfr" class="order-content-el flex gap-3 items-start">
          <div class="order-content-header w-4/12">S&F Request</div>
          <div
            class="order-content-data w-8/12 cursor-pointer"
            @click="redirectToURL(order?.sfr?.url)"
          >
            <div
              class="status px-[0.5rem] py-[0.25rem] border-0 rounded-md"
              :style="{
                'background-color':
                  order?.sfr?.sfr_status?.background_color ?? 'rgb(255, 255, 255)',
                color: order?.sfr?.sfr_status?.color
              }"
            >
              {{ order?.sfr?.reference }}
            </div>
          </div>
        </div>
      </div>
    </div>
    <ArrowProgress></ArrowProgress>
  </div>
</template>

<script lang="ts" setup>
import { computed, onBeforeMount, type PropType, ref } from 'vue';
import type { BaseValidation } from '@vuelidate/core';
import { Button } from 'shared/components';
import { useOrderReferenceStore } from '@/stores/useOrderReferenceStore';
import { useOrderStore } from '@/stores/useOrderStore';
import { useFetch } from '@/composables/useFetch';
import OrderReferences from '@/services/order/order-references';
import { redirectToURL } from '@/helpers';
import { changeColorAlpha } from '@/helpers/colors';
import { addThousandSeparators, toLocalTime } from '@/helpers/order';
import ArrowProgress from '../forms/ArrowProgress.vue';
import Avatar from '../forms/Avatar.vue';
import ButtonPopover from '../forms/ButtonPopover.vue';
import ConfirmSupplierOrderModal from '../modals/ConfirmSupplierOrderModal.vue';
import MarkNoUpliftModal from '../modals/MarkNoUpliftModal.vue';
import SendClientFuelReleaseModal from '../modals/SendClientFuelReleaseModal.vue';
import SendSupplierOrderRequestModal from '../modals/SendSupplierOrderRequestModal.vue';
import SendViaEmailModal from '../modals/SendViaEmailModal.vue';
import SubmitDeliveryTicketDetailsModal from '../modals/SubmitDeliveryTicketDetailsModal.vue';

import type { IOrder, IOrderStatus } from 'shared/types';

const props = defineProps({
  validationInfo: {
    type: Object as PropType<BaseValidation>,
    default: () => null
  },
  isLoading: {
    type: Boolean as PropType<boolean>,
    default: false
  },
  order: {
    type: Object as PropType<IOrder | any>,
    default: null
  }
});

const orderStore = useOrderStore();
const currentStep = computed(() => orderStore.currentStep);

const orderReferenceStore = useOrderReferenceStore();
const quoteButton = computed(() => orderReferenceStore.quoteButton);

const isEmailModalOpened = ref(false);
const isSupplierOrderRequestModalOpened = ref(false);
const isClientFuelReleaseModalOpened = ref(false);
const isMarkNoUpliftModalOpened = ref(false);
const isConfirmSupplierOrderModalOpened = ref(false);
const isSubmitDeliveryTicketDetailsModalOpened = ref(false);

const header = ref<HTMLElement | null>(null);

const { data: orderStatuses, callFetch: fetchOrderStatuses } = useFetch<
  IOrderStatus[],
  () => Promise<IOrderStatus[]>
>(async () => {
  return await OrderReferences.fetchOrderStatuses();
});

function getColor() {
  const status = orderStatuses?.value?.find(
    (el: IOrderStatus) => el.name === props.order?.status?.status_name
  );
  return status?.fill_colour_hex ?? '#fff';
}

function getTextColor() {
  const status = orderStatuses?.value?.find(
    (el: IOrderStatus) => el.name === props.order?.status?.status_name
  );
  return status?.text_colour_hex ?? '#000';
}

const redirectToLinkedOrder = (uri: string) => {
  console.log(uri);
};

onBeforeMount(async () => {
  await Promise.allSettled([fetchOrderStatuses()]);
});

const onProceedToCompliance = () => {
  orderStore.changeStep(2);
};

defineExpose({
  header
});
</script>

<style lang="scss">
.order-header {
  .button {
    background-color: rgba(240, 242, 252, 1) !important;
    color: rgba(81, 93, 138, 1) !important;
    border: 1px solid rgba(81, 93, 138, 0.3) !important;
    @apply flex shrink-0 focus:shadow-none mb-0 mt-0 p-[0.5rem] px-[1rem] rounded-xl #{!important};

    &:hover {
      background-color: rgb(224, 228, 249) !important;
    }

    &-green {
      background-color: rgba(11, 161, 125, 1) !important;
      color: rgba(255, 255, 255, 1) !important;

      &:hover {
        background-color: rgb(13, 196, 152) !important;
      }

      img {
        filter: brightness(0) saturate(100%) invert(100%) sepia(100%) saturate(0%)
          hue-rotate(251deg) brightness(102%) contrast(103%);
      }
    }

    &:disabled {
      background-color: rgba(139, 148, 178, 0.12) !important;
      color: rgb(139, 148, 178) !important;
    }
  }

  .cancel-button {
    background-color: rgb(255, 236, 236) !important;
    color: rgba(254, 98, 98, 1) !important;
    border: 1px solid rgba(254, 98, 98, 0.3) !important;

    img {
      filter: brightness(0) saturate(100%) invert(71%) sepia(81%) saturate(4491%) hue-rotate(321deg)
        brightness(100%) contrast(108%);
    }

    &:hover {
      background-color: rgb(255, 216, 216) !important;
    }
  }

  .send-via-email-popup {
    .el {
      color: theme('colors.main');
      font-size: 16px;
      font-weight: 500;

      &-red {
        color: rgba(254, 98, 98, 1);
      }
    }
  }

  .status {
    font-size: 12px;
  }

  .order-status {
    .status {
      font-size: 16px;
      font-weight: 600;
    }
  }

  .order-name {
    font-size: 22px;
    font-weight: bold;
  }

  .order-linked {
    border: 1px solid rgba(223, 226, 236, 1);
    border-radius: 6px;

    &-text {
      font-size: 12px;
      font-weight: 500;
      color: rgba(82, 90, 122, 1);
    }

    img {
      width: 12px !important;
      height: 12px !important;
    }
  }

  .order-company {
    color: rgba(60, 67, 93, 1);
    font-size: 15px;
    font-weight: 400;
  }

  .order-content-header {
    font-size: 14px;
    color: rgba(82, 90, 122, 1);
  }

  .order-content-data {
    font-size: 16px;
    color: theme('colors.main');
    font-weight: 500;

    &-tooltip {
      display: none;
      position: absolute;
      background-color: rgb(81, 93, 138);
      color: rgb(255, 255, 255);
      font-size: 12px;
      font-weight: 400;
      z-index: 10;
      padding: 0.5rem;
      border-radius: 0.5rem;
      bottom: 2rem;
      right: 0;
      min-width: 30vw;

      &::before {
        content: '';
        position: absolute;
        width: 10px;
        height: 10px;
        background-color: rgb(81, 93, 138);
        transform: rotate(45deg);
        right: 4rem;
        bottom: -5px;
      }
    }
  }

  .hover-wrap {
    &:hover {
      .order-content-data-tooltip {
        display: block;
      }
    }
  }
}
</style>
