<template>
  <div v-if="isOpen" class="order-modal submit-delivery-modal">
    <div class="order-modal-wrapper">
      <div ref="target" class="order-modal-container">
        <div class="order-modal-body">
          <OrderForm add-default-classes>
            <template #header>
              <div class="header w-full flex justify-between">
                <div class="text-[1.25rem] font-medium text-grey-1000">
                  Submit Delivery Ticket Details
                </div>
                <button @click.stop="emit('modal-close')">
                  <img
                    width="12"
                    height="12"
                    src="../../assets/icons/cross.svg"
                    alt="delete"
                    class="close"
                  />
                </button>
              </div>
            </template>
            <template #content>
              <div class="form-body-wrapper flex flex-col items-center">
                <div v-for="(uplift, index) in formModel" :key="index" class="w-full flex flex-col">
                  <Label
                    :required="false"
                    :label-text="`Uplift №${((index as number) + 1)}`"
                    class="whitespace-nowrap"
                  />
                  <SelectField
                    v-model="uplift.aircraft"
                    label-text="Aircraft"
                    placeholder="Select Aircraft"
                    label="display"
                    :options="[]"
                  ></SelectField>
                  <div class="w-full flex gap-x-3 mb-[0.75rem]">
                    <div class="w-6/12 min-w-[132px]">
                      <Label
                        :required="false"
                        label-text="Date & Time of Uplift (UTC)"
                        class="whitespace-nowrap"
                      />
                      <FlatPickr
                        v-if="fromDateTime.length === formModel.length"
                        ref="departureDateRef"
                        v-model="fromDateTime[index as number].date"
                        :config="{
                          allowInput: true,
                          altInput: true,
                          altFormat: 'Y-m-d',
                          dateFormat: 'Y-m-d'
                        }"
                      />
                    </div>
                    <div class="flex flex-col w-6/12">
                      <Label :required="false" label-text="&nbsp;" class="whitespace-nowrap" />
                      <FlatPickr
                        v-if="fromDateTime.length === formModel.length"
                        v-model="fromDateTime[index as number].time"
                        placeholder="Time"
                        :config="{
                          altFormat: 'H:i',
                          altInput: true,
                          allowInput: true,
                          noCalendar: true,
                          enableTime: true,
                          time_24hr: true,
                          minuteIncrement: 1
                        }"
                        class="!pr-0"
                      />
                    </div>
                  </div>
                  <div class="w-full flex gap-3">
                    <InputField
                      v-model="uplift.fuel_quantity"
                      class="w-6/12"
                      :is-validation-dirty="v$?.form?.$dirty"
                      :errors="v$?.form?.jobs?.job_title?.$errors"
                      label-text="Volume Uplifted"
                      placeholder="Please enter quantity"
                    />
                    <SelectField
                      v-model="uplift.fuel_uom"
                      class="w-6/12"
                      label-text="&nbsp;"
                      placeholder=""
                      label="description_plural"
                      :options="fuelQuantityUnits"
                    ></SelectField>
                  </div>
                  <SelectField
                    v-model="uplift.fuel_type"
                    label-text="Fuel Type"
                    placeholder="Select Fuel Type"
                    label="display"
                    :options="[]"
                  ></SelectField>
                  <SelectField
                    v-model="uplift.ipa"
                    label-text="IPA"
                    placeholder="Select IPA"
                    label="display"
                    :options="[]"
                  ></SelectField>
                  <SelectField
                    v-model="uplift.destination"
                    label-text="Destination"
                    placeholder="Select Destination"
                    label="display"
                    :options="[]"
                  ></SelectField>
                  <TextareaField
                    v-model="uplift.comment"
                    class="w-full"
                    :is-validation-dirty="v$?.form?.$dirty"
                    :errors="v$?.form?.jobs?.job_title?.$errors"
                    label-text="Comments"
                    placeholder="Please enter comments"
                  />
                  <div class="flex items-center justify-start mb-[0.75rem] gap-3">
                    <button class="modal-button icon">
                      <img
                        height="20"
                        width="20"
                        :src="getImageUrl('assets/icons/paperclip.svg')"
                        alt="attachment"
                      />
                    </button>
                    <p class="text-base whitespace-nowrap font-semibold text-main">
                      Delivery Ticket
                    </p>
                  </div>
                </div>
                <div class="w-full flex items-center pb-[0.75rem]">
                  <div class="divider-line"></div>
                  <div
                    class="modal-button add gap-2 cursor-pointer"
                    @click="upliftFormStore.addUplift"
                  >
                    <img src="../../assets/icons/plus.svg" alt="add" />
                    Add Another Uplift
                  </div>
                  <div class="divider-line"></div>
                </div>
              </div>
            </template>
          </OrderForm>
        </div>
        <div class="order-modal-footer">
          <button class="modal-button cancel" @click.stop="emit('modal-close')">Cancel</button>
          <button
            class="modal-button submit"
            :disabled="body.length > 200"
            @click.stop="onValidate()"
          >
            Submit
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, watch } from 'vue';
import useVuelidate from '@vuelidate/core';
import { storeToRefs } from 'pinia';
import { useFetch } from 'shared/composables';
import { useUpliftFormStore } from '@/stores/useUpliftFormStore';
import OrderForm from '@/components/forms/OrderForm.vue';
import OrderReferences from '@/services/order/order-references';
import { personRules } from '@/utils/rulesForForms';
import { getImageUrl } from '@/helpers';
import { notify } from '@/helpers/toast';
import FlatPickr from '../FlatPickr/FlatPickr.vue';
import InputField from '../forms/fields/InputField.vue';
import SelectField from '../forms/fields/SelectField.vue';
import TextareaField from '../forms/fields/TextareaField.vue';
import Label from '../forms/Label.vue';

import type { IFuelUom } from 'shared/types';

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  },
  organisationId: {
    type: Number,
    default: 0
  }
});

const emit = defineEmits(['modal-close', 'modal-submit']);

const fromDateTime = ref([
  {
    date: new Date(new Date().getTime() + 24 * 60 * 60 * 1000).toLocaleDateString('en-CA'),
    time: ''
  }
]);

const target = ref(null);

const upliftFormStore = useUpliftFormStore();

const { formModel } = storeToRefs(upliftFormStore);

const validationModel = ref({ form: formModel });

const v$ = ref(useVuelidate(personRules(), validationModel));

const body = ref('');
// onClickOutside(target, () => emit('modal-close'))

const onValidate = async () => {
  const isValid = await v$?.value?.$validate();
  if (!isValid) {
    return notify('Error while submitting, form is not valid!', 'error');
  } else {
    emit('modal-submit');
    emit('modal-close');
  }
};

const { data: fuelQuantityUnits, callFetch: fetchFuelQuantityUnits } = useFetch<IFuelUom[]>(
  async () => {
    return await OrderReferences.fetchFuelQuantityUnits();
  }
);

watch(
  () => [props.organisationId, props.isOpen],
  ([id, isOpen]) => {
    id && isOpen && fetchFuelQuantityUnits();
  }
);

watch(
  () => formModel.value,
  (value: any) => {
    console.log(value);
    if (value.length > fromDateTime.value.length) {
      fromDateTime.value.push({
        date: new Date(new Date().getTime() + 24 * 60 * 60 * 1000).toLocaleDateString('en-CA'),
        time: ''
      });
    }
  }
);
</script>

<style scoped lang="scss">
.submit-delivery-modal {
  .form-body-wrapper {
    max-height: 500px;
  }
  .modal-button {
    display: flex;
    flex-shrink: 0;
    background-color: rgb(81 93 138);
    padding: 0.5rem;
    padding-left: 1rem;
    padding-right: 1rem;
    color: rgb(255 255 255);
    border-radius: 0.5rem;

    &.icon {
      background-color: rgba(240, 242, 252, 1);
      color: rgb(81 93 138);
      padding: 0.75rem;
      border-radius: 0.75rem;
    }

    &.add {
      background-color: transparent;
      color: rgba(81, 93, 138, 1);
      width: fit-content;

      img {
        filter: brightness(0) saturate(100%) invert(37%) sepia(12%) saturate(1572%)
          hue-rotate(190deg) brightness(94%) contrast(89%);
      }
    }
  }

  .divider-line {
    width: 100%;
    min-width: 50px;
    height: 1px;
    border-top: 1px solid rgba(223, 226, 236, 1);
  }
}
</style>
