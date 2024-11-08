<template>
  <div class="w-full h-full flex flex-col gap-2">
    <SendQuoteModal
      ref="quoteModal"
      :is-open="isQuoteModalOpened"
      name="order-modal"
      @modal-close="closeModal"
    />
    <AddServiceCommentModal
      ref="commentModal"
      :is-open="isCommentModalOpened"
      name="order-modal"
      :header="activeService ?? 'Add Comment'"
      @modal-close="closeModal"
    />
    <div class="handling-step bg-white w-full border border-transparent rounded-md">
      <div class="handling-step-header flex justify-between py-[1rem] px-[0.75rem]">
        <div class="handling-step-header-name">Fuel Pricing Details</div>
        <div class="loading-wrap">
          <Loading v-if="false" />
        </div>
      </div>
      <div v-if="true" class="handling-step-content">
        <div class="handling-step-content-header-sub flex">
          <div
            class="handling-step-content-header-sub-wrap flex w-8/12 py-[0.5rem] pl-[0.75rem] gap-2"
          >
            <div class="handling-step-content-header-sub-el flex w-6/12 justify-start">Item</div>
            <div
              class="handling-step-content-header-sub-el flex w-6/12 justify-start el-border pl-4"
            >
              Quantity
            </div>
          </div>
          <div class="handling-step-content-header-sub-wrap flex w-4/12 py-[0.5rem] pl-[0.75rem]">
            <div class="handling-step-content-header-sub-el flex w-full justify-center">
              Arrival
            </div>
            <div class="handling-step-content-header-sub-el flex w-full justify-center">
              Departure
            </div>
            <div class="handling-step-content-header-sub-el flex w-full justify-start">&nbsp;</div>
          </div>
        </div>
        <div
          v-for="(service, index) in mockServices"
          :key="index"
          class="handling-step-content-element flex"
        >
          <div
            class="handling-step-content-element-wrap flex w-8/12 py-[0.5rem] pl-[0.75rem] el-border-light gap-2"
          >
            <div
              class="handling-step-content-element-el-name flex justify-start items-center w-6/12"
            >
              {{ service.name }}
            </div>
            <div class="handling-step-content-element-el flex justify-start items-center w-6/12">
              <span class="text-light-subtitle pr-[0.5rem] text-[0.75rem]">x</span>
              {{ service.quantity ?? '--' }}
              {{ service.time ?? '' }}
            </div>
          </div>
          <div
            class="handling-step-content-element-wrap flex w-4/12 py-[0.75rem] pl-[0.75rem] el-border-light gap-2"
          >
            <div
              class="handling-step-content-element-el-name flex justify-center items-center w-full"
            >
              <CheckboxField
                v-model="service.arrival"
                class="mb-0 mr-1"
                :size="'20px'"
              ></CheckboxField>
            </div>
            <div class="handling-step-content-element-el flex justify-center items-center w-full">
              <CheckboxField
                v-model="service.departure"
                class="mb-0 mr-1"
                :size="'20px'"
              ></CheckboxField>
            </div>
            <div
              class="handling-step-content-element-el flex justify-start items-center w-full px-[0.5rem]"
            >
              <img
                width="20"
                height="20"
                src="../../assets/icons/message-plus-square.svg"
                alt="comment"
                class="cursor-pointer"
                @click="openCommentModal(index)"
              />
            </div>
          </div>
        </div>
        <div
          v-for="(newService, index) in newServices"
          :key="index"
          class="handling-step-content-element flex"
        >
          <div
            class="handling-step-content-element-wrap flex w-8/12 py-[0.5rem] pl-[0.75rem] el-border-light gap-2"
          >
            <div
              class="handling-step-content-element-el-name flex justify-center items-center w-6/12"
            >
              <SelectField
                class="w-full mb-0"
                :is-white="true"
                placeholder="Choose Service"
                :options="displayServices"
                label="name"
                :model-value="newService.name"
                @update:model-value="
                  (value) => {
                    newService.name = value;
                  }
                "
                @search="handleServiceSearch($event)"
              />
            </div>
            <div class="handling-step-content-element-el flex justify-start items-center w-6/12">
              <div class="input-wrap flex items-center pr-[0.75rem]">
                <span class="text-light-subtitle pr-[0.5rem] text-[0.75rem]">x</span>
                <InputField
                  :model-value="newService.quantity"
                  class="w-6/12 mb-0"
                  :is-white="true"
                  :is-half="true"
                  placeholder=" "
                  @update:model-value="
                    (value) => {
                      newService.quantity = value;
                    }
                  "
                />
                <SelectField
                  class="w-6/12 mb-0"
                  :is-white="true"
                  :is-half="true"
                  placeholder=" "
                  :options="['Minutes', 'Hours', 'Days']"
                  label="description_short"
                  :model-value="newService.time"
                  @update:model-value="
                    (value) => {
                      newService.time = value;
                    }
                  "
                />
              </div>
            </div>
          </div>
          <div
            class="handling-step-content-element-wrap flex w-4/12 py-[0.5rem] pl-[0.75rem] el-border-light gap-2"
          >
            <div
              class="handling-step-content-element-el-name flex justify-center items-center w-full"
            >
              <CheckboxField
                v-model="newService.arrival"
                class="mb-0 mr-1"
                :size="'20px'"
              ></CheckboxField>
            </div>
            <div class="handling-step-content-element-el flex justify-center items-center w-full">
              <CheckboxField
                v-model="newService.departure"
                class="mb-0 mr-1"
                :size="'20px'"
              ></CheckboxField>
            </div>
            <div
              class="handling-step-content-element-el flex justify-between items-center w-full px-[0.5rem]"
            >
              <img
                width="20"
                height="20"
                src="../../assets/icons/message-plus-square.svg"
                alt="comment"
                class="cursor-pointer"
                @click="openCommentModal(index, true)"
              />
              <img
                width="20"
                height="20"
                src="../../assets/icons/cross-red.svg"
                alt="delete"
                class="cursor-pointer"
                @click="deleteService(index)"
              />
            </div>
          </div>
        </div>
        <div
          class="handling-step-add-service flex cursor-pointer p-[0.75rem] gap-2 w-fit"
          @click="addNewService"
        >
          <img src="../../assets/icons/plus.svg" alt="add" />
          Add Service to Order
        </div>
      </div>
    </div>
    <div class="handling-step bg-white w-full border border-transparent rounded-md">
      <div class="handling-step-header flex justify-between py-[0.5rem] px-[0.75rem]">
        <div class="handling-step-header-name">Ground Handling Quotes</div>
        <Button class="button flex items-center gap-2" @click="openQuoteModal">
          Send Quote Request
        </Button>
      </div>
      <div class="handling-step-content w-full flex flex-col">
        <div class="handling-step-content-header-wrap w-full flex items-center">
          <div class="handling-step-content-col w-3/12">
            <div class="handling-step-content-col-header px-[0.75rem] py-[0.5rem]">
              Station Name
            </div>
          </div>
          <div class="handling-step-content-col w-3/12">
            <div class="handling-step-content-col-header px-[0.75rem] py-[0.5rem]">Brand</div>
          </div>
          <div class="handling-step-content-col w-2/12">
            <div class="handling-step-content-col-header px-[0.75rem] py-[0.5rem]">Status</div>
          </div>
          <div class="handling-step-content-col w-2/12">
            <div class="handling-step-content-col-header px-[0.75rem] py-[0.5rem] text-right">
              Total Cost
            </div>
          </div>
          <div class="handling-step-content-col w-2/12">
            <div class="handling-step-content-col-header px-[0.75rem] py-[0.5rem]">&nbsp;</div>
          </div>
        </div>
        <div
          v-for="(quote, index) in ghQuotes"
          :key="index"
          class="handling-step-content-data-wrap w-full selected-supplier flex items-center"
        >
          <div class="handling-step-content-col w-3/12">
            <div class="handling-step-content-col-data px-[0.75rem] py-[0.5rem]">
              {{ quote.station_name }}
            </div>
          </div>
          <div class="handling-step-content-col w-3/12">
            <div class="handling-step-content-col-data px-[0.75rem] py-[0.5rem]">
              {{ quote.brand }}
            </div>
          </div>
          <div class="handling-step-content-col w-2/12">
            <div class="flex">
              <div
                class="handling-step-content-col-data px-[0.75rem] py-[0rem] rounded-md uppercase max-w-fit"
                :class="{
                  'status-badge-recieved': quote.quote_provided_at,
                  'status-badge-requested': !quote.quote_provided_at
                }"
              >
                {{ quote.quote_provided_at ? 'Recieved' : 'On Request' }}
              </div>
            </div>
          </div>
          <div class="handling-step-content-col w-2/12">
            <div class="handling-step-content-col-data px-[0.75rem] py-[0.5rem] text-right">
              {{ formatNumber(quote.total_cost) ?? '--' }} {{ quote.currency ?? '' }}
            </div>
          </div>
          <div class="handling-step-content-col w-2/12">
            <div
              class="handling-step-content-col-data px-[0.75rem] py-[0.5rem] flex justify-center"
            >
              <Button v-if="!quote.quote_provided_at" class="button light-button" @click="() => {}">
                <img width="20" height="20" :src="getImageUrl('assets/icons/edit.svg')" alt="edit"
              /></Button>
              <div v-else class="flex items-center justify-center p-[0.5rem]" @click="() => {}">
                <img
                  width="20"
                  height="20"
                  :src="getImageUrl('assets/icons/eye.svg')"
                  alt="details"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
      <div
        v-if="groundHandlers?.results?.length === 0"
        class="handling-step-content-none w-full flex py-[1rem] pr-[0.75rem] pl-[2.5rem] flex flex-col"
      >
        <img width="20" height="20" src="../../assets/icons/alert.svg" alt="warn" class="warn" />
        <div class="handling-step-content-none-header">
          There are no supplier ground handlers options available at this location
        </div>
      </div>
      <div v-if="false" class="handling-step-content w-full flex py-8 px-[0.75rem] flex flex-col">
        <Loading />
      </div>
    </div>
    <div class="handling-step bg-white w-full border border-transparent rounded-md">
      <div class="handling-step-header flex justify-between py-[1rem] px-[0.75rem]">
        <div class="handling-step-header-name">Ground Handler Selection</div>
      </div>
      <div class="handling-step-content w-full flex flex-col">
        <div class="handling-step-content-header-wrap w-full flex items-center">
          <div class="handling-step-content-col w-3/12">
            <div class="handling-step-content-col-header px-[0.75rem] py-[0.5rem]">
              Station Name
            </div>
          </div>
          <div class="handling-step-content-col w-2/12">
            <div class="handling-step-content-col-header px-[0.75rem] py-[0.5rem]">Brand</div>
          </div>
          <div class="handling-step-content-col w-1/12">
            <div class="handling-step-content-col-header px-[0.75rem] py-[0.5rem]">
              Handles Mil?
            </div>
          </div>
          <div class="handling-step-content-col w-2/12">
            <div class="handling-step-content-col-header px-[0.75rem] py-[0.5rem]">
              Pricing Details
            </div>
          </div>
          <div class="handling-step-content-col w-2/12">
            <div class="handling-step-content-col-header px-[0.75rem] py-[0.5rem] text-right">
              Estimated Total Cost
            </div>
          </div>
          <div class="handling-step-content-col w-2/12">
            <div class="handling-step-content-col-header px-[0.75rem] py-[0.5rem]">&nbsp;</div>
          </div>
        </div>
        <div
          v-for="(handler, index) in groundHandlers?.results"
          :key="index"
          class="handling-step-content-data-wrap w-full flex items-center"
          :class="{ 'selected-supplier': selectedHandler === index }"
        >
          <div class="handling-step-content-col w-3/12">
            <div class="handling-step-content-col-data px-[0.75rem] py-[0.5rem]">
              {{ handler.station_name }}
            </div>
          </div>
          <div class="handling-step-content-col w-2/12">
            <div class="handling-step-content-col-data px-[0.75rem] py-[0.5rem]">
              {{ handler.brand }}
            </div>
          </div>
          <div class="handling-step-content-col w-1/12">
            <div class="handling-step-content-col-data px-[0.75rem] py-[0.5rem]">
              {{ handler.handles ? 'Yes' : handler.handles === null ? 'TBC' : 'No' }}
            </div>
          </div>
          <div class="handling-step-content-col w-2/12">
            <div
              class="handling-step-content-col-data status-badge px-[0.75rem] py-[0rem] rounded-md uppercase text-center"
              :style="{ background: handler.pricing_details?.background }"
            >
              {{ handler.pricing_details?.status }}
            </div>
          </div>
          <div class="handling-step-content-col w-2/12">
            <div class="handling-step-content-col-data px-[0.75rem] py-[0.5rem] text-right">
              {{ formatNumber(handler.total_cost) ?? '--' }} {{ handler.currency ?? '' }}
            </div>
          </div>
          <div class="handling-step-content-col w-2/12">
            <div
              class="handling-step-content-col-data px-[0.75rem] py-[0.5rem] flex justify-center"
            >
              <Button v-if="selectedHandler === null" class="button" @click="selectHandler(index)"
                >Select</Button
              >
              <div
                v-else
                class="selection-tick flex items-center justify-center"
                @click="selectHandler(null)"
              >
                <img width="20" height="20" src="../../assets/icons/check.svg" alt="check" />
              </div>
            </div>
          </div>
        </div>
      </div>
      <div
        v-if="groundHandlers?.results?.length === 0"
        class="handling-step-content-none w-full flex py-[1rem] pr-[0.75rem] pl-[2.5rem] flex flex-col"
      >
        <img width="20" height="20" src="../../assets/icons/alert.svg" alt="warn" class="warn" />
        <div class="handling-step-content-none-header">
          There are no supplier ground handlers options available at this location
        </div>
      </div>
      <div v-if="false" class="handling-step-content w-full flex py-8 px-[0.75rem] flex flex-col">
        <Loading />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, type PropType, type Ref, ref, watch } from 'vue';
import { Button } from 'shared/components';
import { useFetchHandlingServices } from '@/services/order/fetchers';
import { getImageUrl } from '@/helpers';
import { formatNumber } from '@/helpers/order';
import CheckboxField from '../forms/fields/CheckboxField.vue';
import InputField from '../forms/fields/InputField.vue';
import SelectField from '../forms/fields/SelectField.vue';
import Loading from '../forms/Loading.vue';
import AddServiceCommentModal from '../modals/AddServiceCommentModal.vue';
import SendQuoteModal from '../modals/SendQuoteModal.vue';

import type { IOrder } from 'shared/types';

const props = defineProps({
  isLoading: {
    type: Boolean as PropType<boolean>,
    default: false
  },
  order: {
    type: Object as PropType<IOrder>,
    default: null
  }
});

const groundHandlers = {
  results: [
    {
      station_name: 'Signature LBG (Terminal 1)',
      brand: 'Signature Flight Support',
      handles: true,
      pricing_details: { background: 'rgba(254, 161, 22, 1)', status: 'Historical Invoice' },
      total_cost: '$1,650',
      currency: 'USD'
    },
    {
      station_name: 'Signature LBG (Terminal 1)',
      brand: 'Signature Flight Support',
      handles: true,
      pricing_details: { background: 'rgba(11, 161, 125, 1)', status: 'Historical Invoice' },
      total_cost: '$1,650',
      currency: 'USD'
    },
    {
      station_name: 'Signature LBG (Terminal 1)',
      brand: 'Signature Flight Support',
      handles: true,
      pricing_details: { background: 'rgba(221, 44, 65, 1)', status: 'Historical Invoice' },
      total_cost: '$1,650',
      currency: 'USD'
    }
  ]
};

const ghQuotes = [
  {
    station_name: 'Signature LBG (Terminal 1)',
    brand: 'Signature Flight Support',
    quote_provided_at: '123',
    total_cost: '$1,650',
    currency: 'USD'
  },
  {
    station_name: 'Signature LBG (Terminal 1)',
    brand: 'Signature Flight Support',
    quote_provided_at: null,
    total_cost: '$1,650',
    currency: 'USD'
  }
];

const mockServices = ref([
  { name: 'Handling Fee', quantity: null, time: null, arrival: true, departure: true },
  { name: 'Passenger Handling', quantity: null, time: null, arrival: true, departure: false },
  { name: 'Parking', quantity: 3, time: 'Hours', arrival: true, departure: true }
]);

const userService = ref([{ name: '' }]);
const displayServices = computed(() => [...userService.value, ...handlingServices.value]);

const newServices: Ref<Array<any>> = ref([]);
const activeService: Ref<string | null> = ref(null);
const isQuoteModalOpened = ref(false);
const isCommentModalOpened = ref(false);

const openQuoteModal = () => {
  isQuoteModalOpened.value = true;
};
const openCommentModal = (index: number, isNew = false) => {
  isNew
    ? (activeService.value = newServices.value[index].name)
    : (activeService.value = mockServices.value[index].name);
  isCommentModalOpened.value = true;
};
const closeModal = () => {
  isQuoteModalOpened.value = false;
  isCommentModalOpened.value = false;
};

const selectedHandler: Ref<number | null> = ref(null);
const selectHandler = async (id: number | null) => {
  selectedHandler.value = id;
};

const addNewService = () => {
  newServices.value.push({
    name: '',
    quantity: null,
    time: null,
    arrival: false,
    departure: false
  });
};

const deleteService = (id: number) => {
  newServices.value.splice(id, 1);
};

const { callFetch: fetchHandlingServices, data: handlingServices } = useFetchHandlingServices();

const handleServiceSearch = (searchTerm: string) => {
  // console.log(searchTerm, index);
  userService.value = [{ name: searchTerm }];
};

watch(
  () => props.order,
  async (order: IOrder) => {
    if (order && order.type.is_gh) {
      await fetchHandlingServices();
    }
  }
);
</script>

<style lang="scss">
.handling-step {
  .button {
    background-color: rgba(81, 93, 138, 1) !important;
    color: white !important;
    font-weight: 500 !important;
    font-size: 16px !important;
    @apply flex shrink-0 focus:shadow-none mb-0 mt-0 p-[0.5rem] px-[1rem] rounded-xl #{!important};

    &:disabled {
      background-color: rgb(190, 196, 217) !important;
      color: rgb(133, 141, 173) !important;
      border: transparent !important;
    }

    &.light-button {
      background-color: rgba(240, 242, 252, 1) !important;
      border: transparent !important;
      padding: 0.5rem !important;
    }
  }

  .el-border {
    border-right: 1px solid rgb(223, 226, 236);

    &-light {
      border-right: 1px solid theme('colors.dark-background');
    }
  }

  .hover-wrap {
    &:hover {
      .handling-step-tooltip {
        display: block;
      }
    }
  }

  &-add-service {
    color: rgba(81, 93, 138, 1);
    font-weight: 500;
    font-size: 14px;
    img {
      filter: brightness(0) saturate(100%) invert(36%) sepia(11%) saturate(1776%) hue-rotate(190deg)
        brightness(94%) contrast(86%);
    }
  }

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
    top: 2.5rem;
    right: 0;
    min-width: 30vw;

    &::before {
      content: '';
      position: absolute;
      width: 10px;
      height: 10px;
      background-color: rgb(81, 93, 138);
      transform: rotate(45deg);
      right: 1.9rem;
      top: -5px;
    }

    &.right-tooltip {
      left: 0;
      top: 1.6rem;
      min-width: 10vw;

      &::before {
        right: 0;
        left: 1rem;
      }
    }
  }

  &-header {
    color: theme('colors.main');
    font-size: 18px;
    font-weight: 600;
  }

  &-content {
    &-data-wrap {
      border-bottom: 1px solid theme('colors.dark-background');
      background-color: rgba(246, 248, 252, 0.5);

      &:last-of-type {
        border-radius: 0 0 8px 8px;
      }

      &.selected-supplier {
        background-color: rgba(255, 255, 255, 1) !important;

        .handling-step-content-col-data {
          color: rgba(39, 44, 63, 1);
          background-color: rgba(255, 255, 255, 1);

          .warn {
            filter: none;
          }

          .selection-tick {
            display: flex;
            border-radius: 12px;
            background-color: rgba(11, 161, 125, 0.15);
            height: 40px;
            width: 40px;
            opacity: 1;
          }
        }
      }
    }

    &-header-wrap {
      background-color: rgb(246, 248, 252);
    }

    &-header-big-wrap {
      background-color: rgba(246, 248, 252, 1);
    }

    &-header-big {
      &-el {
        background-color: rgba(223, 226, 236, 0.5);
        color: rgba(39, 44, 63, 1);
        font-size: 12px;
        font-weight: 500;
      }
    }

    &-header-sub {
      background-color: rgba(246, 248, 252, 1);

      &-el {
        color: rgba(82, 90, 122, 1);
        font-size: 11px;
        font-weight: 500;
      }
    }

    &-element {
      &-wrap {
        border-bottom: 1px solid rgba(246, 248, 252, 1);
      }

      &-el {
        color: rgba(39, 44, 63, 1);
        font-size: 13px;
        font-weight: 400;

        &-name {
          color: rgba(39, 44, 63, 1);
          font-size: 13px;
          font-weight: 500;
        }
      }
    }

    &-results {
      background-color: rgba(246, 248, 252, 1);

      &-el {
        &-name {
          color: rgba(82, 90, 122, 1);
          font-size: 11px;
          font-weight: 500;
          border-left: 1px solid rgb(223, 226, 236);
        }

        &-value {
          color: rgba(39, 44, 63, 1);
          font-size: 13px;
          font-weight: 600;
        }
      }
    }

    &-divider {
      text-transform: capitalize;
      background-color: rgba(246, 248, 252, 1);
      color: rgba(82, 90, 122, 1);
      font-size: 12px;
      font-weight: 500;
    }

    &-margin {
      &-name {
        color: rgba(39, 44, 63, 1);
        font-size: 13px;
        font-weight: 500;
      }

      &-value {
        color: rgba(11, 161, 125, 1);
        font-size: 16px;
        font-weight: 600;
      }
    }

    &-col {
      height: 100%;

      &-header {
        color: rgba(82, 90, 122, 1);
        font-size: 11px;
        font-weight: 500;
        background-color: rgb(246, 248, 252);
      }

      &-data {
        color: rgba(133, 141, 173, 1);
        font-size: 13px;
        font-weight: 400;

        .warn {
          filter: brightness(0) saturate(100%) invert(89%) sepia(7%) saturate(740%)
            hue-rotate(193deg) brightness(88%) contrast(92%);
        }

        .selection-tick {
          opacity: 0;
          height: 40px;
          width: 40px;
        }

        .files-button {
          border: 1px solid rgba(223, 226, 236, 1);
          border-radius: 6px;
        }

        .horizontal {
          transform: rotate(90deg);
        }

        &.status-badge {
          color: rgba(255, 255, 255) !important;

          &-recieved {
            background-color: rgba(11, 161, 125, 0.12) !important;
            color: rgba(11, 161, 125, 1) !important;
          }
          &-requested {
            background-color: rgba(254, 161, 22, 0.12) !important;
            color: rgba(254, 161, 22, 1) !important;
          }
        }
      }
    }

    &-none {
      position: relative;
      background-color: rgba(255, 161, 0, 0.08);

      &-header {
        color: theme('colors.main');
        font-size: 14px;
        font-weight: 600;
      }

      &-desc {
        color: theme('colors.main');
        font-size: 12px;
        font-weight: 400;
      }

      .warn {
        position: absolute;
        left: 0.75rem;
      }
    }

    &-missing {
      background-color: rgba(246, 248, 252, 1);

      span {
        color: rgba(82, 90, 122, 1);
        font-size: 11px;
        font-weight: 500;
      }
    }
  }

  .roi {
    border-top: 1px solid theme('colors.dark-background');

    &-inputs-wrap:first-of-type {
      border-right: 1px solid theme('colors.dark-background');
    }

    &-results {
      background-color: rgba(246, 248, 252, 1);

      &-wrap {
        background-color: rgba(246, 248, 252, 1);

        &:first-of-type {
          border-right: 1px solid rgba(223, 226, 236, 1);
        }
      }

      &-label {
        color: rgba(82, 90, 122, 1);
        font-size: 16px;
        font-weight: 500;
      }

      &-value {
        color: rgba(39, 44, 63, 1);
        font-size: 16px;
        font-weight: 600;

        &-green {
          color: rgba(255, 255, 255, 1);
          background-color: rgba(11, 161, 125, 1);
          border-radius: 6px;
          padding: 6px 12px;
        }
      }
    }

    &-input {
      flex-direction: row;
      margin-bottom: 0 !important;
    }

    &-label {
      color: rgba(82, 90, 122, 1);
      font-size: 11px;
      font-weight: 500;
    }
  }
}
</style>
