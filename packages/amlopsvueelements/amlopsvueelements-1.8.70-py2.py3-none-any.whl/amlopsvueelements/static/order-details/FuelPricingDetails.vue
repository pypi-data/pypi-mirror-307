<template>
  <div class="pricing-step bg-white w-full border border-transparent rounded-md">
    <div class="pricing-step-header flex justify-between py-[1rem] px-[0.75rem]">
      <div class="pricing-step-header-name">Fuel Pricing Details</div>
      <div class="loading-wrap">
        <Loading v-if="isLoading" />
      </div>
    </div>
    <div v-if="orderPricing && order && orderPricing.supplier_id" class="pricing-step-content">
      <div class="pricing-step-content-header-big-wrap flex">
        <div class="pricing-step-content-header-big flex w-4/12"></div>
        <div class="pricing-step-content-header-big flex w-4/12 p-1">
          <div class="pricing-step-content-header-big-el flex w-full py-1 justify-center rounded">
            Supplier Pricing
          </div>
        </div>
        <div class="pricing-step-content-header-big flex w-4/12 p-1">
          <div class="pricing-step-content-header-big-el flex w-full py-1 justify-center rounded">
            Client Pricing
          </div>
        </div>
      </div>
      <div class="pricing-step-content-header-sub flex">
        <div
          class="pricing-step-content-header-sub-wrap flex w-4/12 py-[0.5rem] pl-[0.75rem] gap-2"
        >
          <div class="pricing-step-content-header-sub-el flex w-8/12 justify-start">Item</div>
          <div class="pricing-step-content-header-sub-el flex w-4/12 justify-start el-border">
            Quantity
          </div>
        </div>
        <div class="pricing-step-content-header-sub-wrap flex w-4/12 py-[0.5rem] pl-[0.75rem]">
          <div class="pricing-step-content-header-sub-el flex w-full justify-start">Unit Price</div>
          <div class="pricing-step-content-header-sub-el flex w-full justify-start el-border">
            Total Cost
          </div>
        </div>
        <div class="pricing-step-content-header-sub-wrap flex w-4/12 p-[0.5rem] pl-[0.75rem]">
          <div class="pricing-step-content-header-sub-el flex w-full justify-start">Unit Price</div>
          <div class="pricing-step-content-header-sub-el flex w-full justify-start">Total Cost</div>
        </div>
      </div>
      <div class="pricing-step-content-element flex">
        <div
          class="pricing-step-content-element-wrap flex w-4/12 py-[0.5rem] pl-[0.75rem] el-border-light gap-2"
        >
          <div class="pricing-step-content-element-el-name flex justify-start items-center w-8/12">
            {{ props.order?.fuel_order?.fuel_category?.name }}
          </div>
          <div class="pricing-step-content-element-el flex justify-start items-center w-4/12">
            {{ addThousandSeparators(props.order?.fuel_order?.fuel_quantity) }} ({{
              props.order?.fuel_order?.fuel_uom?.description_plural
            }})
          </div>
        </div>
        <div
          class="pricing-step-content-element-wrap flex w-4/12 py-[0.5rem] pl-[0.75rem] el-border-light"
        >
          <div class="pricing-step-content-element-el flex w-full justify-start items-center">
            {{ parseFloat(orderPricing?.fuel_pricing?.supplier?.unit_price_amount) }}
            {{ orderPricing?.fuel_pricing?.supplier?.unit_price_pricing_unit?.description_short }}
          </div>
          <div class="pricing-step-content-element-el flex w-full justify-start items-center">
            {{ formatNumber(orderPricing?.fuel_pricing?.supplier?.amount_total) }}
            {{ orderPricing?.fuel_pricing?.supplier?.amount_currency?.code }}
          </div>
        </div>
        <div class="pricing-step-content-element-wrap flex w-4/12 py-[0.5rem] pl-[0.75rem]">
          <div class="pricing-step-content-element-el flex w-full justify-start items-center">
            <div class="input-wrap flex pr-[0.75rem]">
              <InputField
                :model-value="
                  removeTrailingZeros(orderPricing.fuel_pricing?.client?.unit_price_amount)
                "
                class="w-6/12 mb-0"
                :is-white="true"
                :is-half="true"
                placeholder=" "
                @update:model-value="onPriceChange($event)"
              />
              <SelectField
                class="w-6/12 mb-0"
                :is-white="true"
                :is-half="true"
                placeholder="Select activity type"
                :options="[orderPricing.fuel_pricing?.client?.unit_price_pricing_unit]"
                label="description_short"
                :model-value="orderPricing.fuel_pricing?.client?.unit_price_pricing_unit"
                :disabled="true"
              />
            </div>
          </div>
          <div
            class="pricing-step-content-element-el flex w-full justify-start items-center pr-[0.75rem]"
          >
            <InputField
              :model-value="formatNumber(orderPricing.fuel_pricing?.client?.amount_total)"
              class="roi-input w-full"
              :is-white="true"
              placeholder=" "
              :disabled="true"
            >
              <template #suffix>{{
                orderPricing.fuel_pricing?.client?.amount_currency?.code
              }}</template>
            </InputField>
          </div>
        </div>
      </div>
      <div
        v-if="orderPricing && orderPricing.fees?.length > 0"
        class="pricing-step-content-divider flex w-full py-[0.5rem] px-[0.75rem]"
      >
        Fees
      </div>
      <div
        v-for="(fee, key) in orderPricing.fees"
        v-if="orderPricing && orderPricing.fees.length > 0"
        :key="key"
        class="pricing-step-content-element flex"
      >
        <div
          class="pricing-step-content-element-wrap flex w-4/12 py-[0.5rem] pl-[0.75rem] el-border-light gap-2"
        >
          <div class="pricing-step-content-element-el-name flex justify-start items-center w-8/12">
            {{
              fee.supplier?.suppliers_fuel_fees_rates_row?.supplier_fuel_fee?.fuel_fee_category
                ?.name ?? 'Fee'
            }}
          </div>
          <div class="pricing-step-content-element-el flex justify-start items-center w-4/12">
            x {{ parseInt(fee.supplier?.quantity_value) }}
          </div>
        </div>
        <div
          class="pricing-step-content-element-wrap flex w-4/12 py-[0.5rem] pl-[0.75rem] el-border-light"
        >
          <div class="pricing-step-content-element-el flex w-full justify-start items-center">
            {{ formatNumber(parseFloat(fee.supplier?.unit_price_amount).toFixed(2)) }}
            {{ fee.supplier?.unit_price_pricing_unit?.description_short }}
          </div>
          <div class="pricing-step-content-element-el flex w-full justify-start items-center">
            {{ formatNumber(parseFloat(fee.supplier?.amount_total).toFixed(2)) }}
            {{ fee.supplier?.amount_currency?.code }}
          </div>
        </div>
        <div class="pricing-step-content-element-wrap flex w-4/12 py-[0.5rem] pl-[0.75rem]">
          <div class="pricing-step-content-element-el flex w-full justify-start items-center">
            <div class="input-wrap flex pr-[0.75rem]">
              <InputField
                :model-value="removeTrailingZeros(fee.client?.unit_price_amount)"
                class="w-6/12 mb-0"
                :is-white="true"
                :is-half="true"
                placeholder=" "
                @update:model-value="onFeeChange($event, key)"
              />
              <SelectField
                class="w-6/12 mb-0"
                :is-white="true"
                :is-half="true"
                placeholder=" "
                :options="[fee.client?.unit_price_pricing_unit]"
                label="description_short"
                :model-value="fee.client?.unit_price_pricing_unit"
                :disabled="true"
              />
            </div>
          </div>
          <div
            class="pricing-step-content-element-el flex w-full justify-start items-center pr-[0.75rem]"
          >
            <InputField
              class="roi-input w-full"
              :model-value="formatNumber(fee?.client?.amount_total)"
              :is-white="true"
              placeholder=" "
              :disabled="true"
            >
              <template #suffix>{{
                fee?.client?.unit_price_pricing_unit?.currency?.code
              }}</template>
            </InputField>
          </div>
        </div>
      </div>
      <div
        v-if="orderPricing && orderPricing.taxes.length > 0"
        class="pricing-step-content-divider flex w-full py-[0.5rem] px-[0.75rem]"
      >
        Taxes
      </div>
      <div
        v-for="(tax, key) in orderPricing.taxes"
        v-if="orderPricing && orderPricing.taxes.length > 0"
        :key="key"
        class="pricing-step-content-element flex"
      >
        <div
          class="pricing-step-content-element-wrap flex w-4/12 py-[0.5rem] pl-[0.75rem] el-border-light gap-2"
        >
          <div
            class="pricing-step-content-element-el-name flex justify-start items-center w-8/12 gap-1 relative"
          >
            {{ tax.supplier?.tax?.category?.name ?? 'Tax' }}
            <div class="pricing-step-content-block-body-note hover-wrap contents flex items-center">
              <img
                width="12"
                height="12"
                src="../../assets/icons/info-circle.svg"
                alt="warn"
                class="warn"
              />
              <div class="pricing-step-tooltip right-tooltip">
                ● Applies on:
                {{
                  tax.supplier.applies_on?.fuel
                    ? 'Fuel'
                    : tax.supplier.applies_on?.fees
                    ? Object.values(tax.supplier.applies_on?.fees)[0]
                    : tax.supplier.applies_on?.taxes
                    ? tax.supplier.applies_on?.taxes
                    : ''
                }}
              </div>
            </div>
          </div>
          <div class="pricing-step-content-element-el flex justify-start items-center w-4/12">
            x 1
          </div>
        </div>
        <div
          class="pricing-step-content-element-wrap flex w-4/12 py-[0.5rem] pl-[0.75rem] el-border-light"
        >
          <div class="pricing-step-content-element-el flex w-full justify-start items-center">
            {{ tax?.supplier?.tax_percentage ? `${tax?.supplier?.tax_percentage}%` : '-' }}
          </div>
          <div class="pricing-step-content-element-el flex w-full justify-start items-center">
            {{ formatNumber(tax?.supplier?.tax_amount_total) }}
            {{ tax?.supplier?.tax_amount_currency?.code }}
          </div>
        </div>
        <div class="pricing-step-content-element-wrap flex w-4/12 py-[0.5rem] pl-[0.75rem]">
          <div class="pricing-step-content-element-el flex w-full justify-start items-center">
            {{ tax?.client?.tax_percentage ? `${tax?.client?.tax_percentage}%` : '-' }}
          </div>
          <div class="pricing-step-content-element-el flex w-full justify-start items-center">
            {{ formatNumber(tax?.client?.tax_amount_total) }}
            {{ tax?.client?.tax_amount_currency?.code }}
          </div>
        </div>
      </div>
      <div class="pricing-step-content-results flex">
        <div class="pricing-step-content-results-wrap flex w-4/12 py-[0.5rem] pl-[0.75rem]"></div>
        <div class="pricing-step-content-results-wrap flex w-4/12 py-[0.5rem]">
          <div
            class="pricing-step-content-results-el-name flex items-center w-full p-1 pl-[0.75rem] justify-start items-center"
          >
            Total Buy Price
          </div>
          <div
            class="pricing-step-content-results-el-value flex w-full p-1 justify-start items-center"
          >
            {{ formatNumber(orderPricing?.pricing_summary?.supplier_total) }}
            {{ orderPricing.fuel_pricing?.supplier?.amount_currency?.code }}
          </div>
        </div>
        <div class="pricing-step-content-results-wrap flex w-4/12 py-[0.5rem]">
          <div
            class="pricing-step-content-results-el-name flex items-center w-full p-1 pl-[0.75rem] justify-start items-center"
          >
            Total Sell Price
          </div>
          <div
            class="pricing-step-content-results-el-value flex w-full p-1 justify-start items-center"
          >
            {{ formatNumber(orderPricing?.pricing_summary?.client_total) }}
            {{ orderPricing.fuel_pricing?.client?.amount_currency?.code }}
          </div>
        </div>
      </div>
      <div class="pricing-step-content-margin flex p-3">
        <div class="pricing-step-content-margin-name w-6/12 flex items-center">Margin</div>
        <div class="pricing-step-content-margin-value w-6/12 flex items-center pl-2">
          {{ formatNumber(orderPricing?.pricing_summary?.margin_amount) }}
          {{ orderPricing?.fuel_pricing?.client?.amount_currency?.code }} ({{
            orderPricing?.pricing_summary?.margin_percentage
          }}%)
        </div>
      </div>
    </div>
    <div v-else class="pricing-step-content-missing flex items-center justify-center py-[1.25rem]">
      <Loading v-if="isLoading" />
      <span v-else>Please select a Fuel Supply option</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useDebounceFn } from '@vueuse/core';
import { storeToRefs } from 'pinia';
import { useOrderReferenceStore } from '@/stores/useOrderReferenceStore';
import { addThousandSeparators, formatNumber, removeTrailingZeros } from '@/helpers/order';
import InputField from '../forms/fields/InputField.vue';
import SelectField from '../forms/fields/SelectField.vue';
import Loading from '../forms/Loading.vue';

import type { IOrder } from 'shared/types';

type Props = {
  order: IOrder | null;
  isLoading: boolean;
  isLoadingUpdateOrderPricing: boolean;
};

const props = defineProps<Props>();

const orderReferenceStore = useOrderReferenceStore();

const { orderPricing } = storeToRefs(orderReferenceStore);
const { onUpdateOrderPricing, onUpdateOrderRoi } = orderReferenceStore;

const onPriceChange = useDebounceFn(async (value: any) => {
  orderPricing.value!.fuel_pricing.client.unit_price_amount = value;
  await onUpdateOrderPricing();
  await onUpdateOrderRoi();
}, 1000);

const onFeeChange = useDebounceFn(async (value: any, index: number) => {
  orderPricing.value!.fees[index].client.unit_price_amount = value;
  await onUpdateOrderPricing();
  await onUpdateOrderRoi();
}, 1000);
</script>
