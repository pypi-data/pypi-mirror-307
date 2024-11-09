<template>
  <div v-if="isOpen" class="order-modal add-activity-modal">
    <div class="order-modal-wrapper">
      <div class="order-modal-container">
        <div class="order-modal-body">
          <OrderForm>
            <template #header>
              <div class="header w-full flex justify-between">
                <div class="text-[1.25rem] font-medium text-grey-1000">Add CRM Activity</div>
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
              <ScrollBar>
                <div class="form-body-wrapper px-6 py-[0.5rem]">
                  <TextareaField
                    v-model="description"
                    class="w-full"
                    label-text="Description"
                    :required="true"
                    placeholder="Add activity description"
                  />
                  <Label :required="true" label-text="Datetime" />
                  <div class="flex items-center gap-[1rem] mt-[0.25rem] mb-[0.75rem] w-full">
                    <FlatPickr
                      v-model="fromDateTime.date"
                      :config="{
                        allowInput: true,
                        altInput: true,
                        altFormat: 'Y-m-d',
                        dateFormat: 'Y-m-d'
                      }"
                    />
                    <FlatPickr
                      v-model="fromDateTime.time"
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
                  <div class="mt-[0.25rem] mb-[0.75rem] w-full">
                    <Loading v-if="isTypesPending" />
                    <SelectField
                      v-else
                      v-model="activityType"
                      label-text="Activity Type"
                      :required="true"
                      class="w-6/12"
                      placeholder=""
                      label="description_plural"
                      :options="activityTypeOptions"
                    ></SelectField>
                  </div>
                </div>
              </ScrollBar>
            </template>
          </OrderForm>
        </div>
        <div class="order-modal-footer">
          <button class="modal-button cancel" @click.stop="emit('modal-close')">Close</button>
          <Loading v-if="isAddActivityPending" />
          <button v-else class="modal-button submit" @click.stop="onSave()">Save</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { computed, ref } from 'vue';
import { useQueryClient } from '@tanstack/vue-query';
import OrderForm from '@/components/forms/OrderForm.vue';
import { useMutationAddCRMActivity } from '@/services/mutations/crm-activity';
import { useQueryCRMActivityTypes } from '@/services/queries';
import { notify } from '@/helpers/toast';
import FlatPickr from '../FlatPickr/FlatPickr.vue';
import SelectField from '../forms/fields/SelectField.vue';
import TextareaField from '../forms/fields/TextareaField.vue';
import Label from '../forms/Label.vue';
import Loading from '../forms/Loading.vue';
import ScrollBar from '../forms/ScrollBar.vue';

type Props = {
  isOpen: boolean;
  orderId: number;
};

const props = defineProps<Props>();

const emit = defineEmits(['modal-close', 'modal-submit']);

const queryClient = useQueryClient();

const { data: crmActivityTypes, isPending: isTypesPending } = useQueryCRMActivityTypes();
const { mutate: addCRMActivityMutation, isPending: isAddActivityPending } =
  useMutationAddCRMActivity();

const description = ref('');
const activityType = ref<string>();
const fromDateTime = ref({
  date: new Date().toLocaleDateString('en-CA'),
  time: ''
});
const activityTypeOptions = computed(() => crmActivityTypes.value?.map((type) => type.name) ?? []);

const hasError = () => {
  let error = '';

  if (!activityType.value) error = 'Activity Type is required';
  if (!fromDateTime.value.date || !fromDateTime.value.time) error = 'Date and time are required';
  if (!description.value) error = 'Description is required';

  if (error) notify(error, 'error');
  return error;
};

const onSave = async () => {
  if (hasError()) return;

  const activityTypeId = crmActivityTypes.value?.find(
    (type) => type.name === activityType.value
  )?.id;

  if (!activityTypeId) {
    notify('Invalid activity type', 'error');
    return;
  }

  await addCRMActivityMutation(
    {
      orderId: props.orderId,
      payload: {
        description: description.value,
        activity_type: activityTypeId,
        datetime: `${fromDateTime.value.date} ${fromDateTime.value.time}`
      }
    },
    {
      onSuccess: () => {
        queryClient.invalidateQueries({ queryKey: ['CRMActivity', props.orderId] });
        emit('modal-close');
      }
    }
  );
};
</script>

<style scoped lang="scss">
.add-activity-modal {
  &-checkbox {
    margin-bottom: 0;
  }
}
</style>
