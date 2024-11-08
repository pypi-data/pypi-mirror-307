<template>
  <div v-if="isOpen" class="order-modal quote-modal">
    <div class="order-modal-wrapper">
      <div ref="target" class="order-modal-container">
        <div class="order-modal-body">
          <OrderForm add-default-classes>
            <template #header>
              <div class="header w-full flex justify-between">
                <div class="text-[1.25rem] font-medium text-grey-1000">
                  Send Ground Handling Quote Request(s)
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
              <ScrollBar>
                <div class="form-body-wrapper">
                  <div class="quote-modal-text">
                    <div class="quote-modal-text-content text-main font-semibold font-size-[15px]">
                      Select ground handler(s) to request a quote
                    </div>
                    <div class="quote-modal-text-description text-subtitle">
                      Please make sure that all required services have been added to the order
                      before sending the quote requests out.
                    </div>
                  </div>
                  <div class="flex flex-col mt-[1.5rem] mb-[0.75rem] pl-[0.5rem] w-full">
                    <div class="flex items-start justify-start pb-[1rem]">
                      <CheckboxField v-model="isPinned" class="mb-0 mt-[2px] mr-[0.25rem]" />
                      <div class="checkbox-text flex flex-col gap-2">
                        <div
                          class="text-base whitespace-nowrap font-semibold text-main relative flex gap-1"
                        >
                          Signature LBG (Terminal 1)
                          <div
                            v-if="!email || !isValidEmail"
                            class="quote-modal-tooltip-body hover-wrap contents flex items-center"
                          >
                            <img
                              width="12"
                              height="12"
                              src="../../assets/icons/info-circle.svg"
                              alt="warn"
                              class="filter-red"
                            />
                            <div class="quote-modal-tooltip">
                              {{
                                !email
                                  ? 'Email address missing'
                                  : !isValidEmail
                                  ? 'Invalid email'
                                  : ''
                              }}
                            </div>
                          </div>
                        </div>
                        <InputField v-if="isPinned" v-model="email" class="mb-0" />
                      </div>
                    </div>
                    <div class="flex items-start justify-start pb-[1rem]">
                      <CheckboxField class="mb-0 mt-[2px] mr-[0.25rem]" />
                      <div class="checkbox-text flex items-center gap-2">
                        <p class="text-base whitespace-nowrap font-semibold text-main">
                          ASTONSKY Paris Le Bourget
                        </p>
                      </div>
                    </div>
                    <div class="flex items-start justify-start pb-[1rem]">
                      <div class="mb-0 mt-[2px] mr-[0.5rem]">
                        <img
                          width="20"
                          height="20"
                          :src="getImageUrl('assets/icons/quote_checkbox_requested.svg')"
                          alt="checkbox"
                        />
                      </div>

                      <div class="checkbox-text flex items-center gap-2">
                        <p class="text-base whitespace-nowrap font-semibold text-main">
                          Jetex FBO, Paris
                        </p>
                        <p class="text-sm whitespace-nowrap text-subtitle">(Waiting for Quote)</p>
                      </div>
                    </div>
                    <div class="flex items-start justify-start pb-[1rem]">
                      <div class="mb-0 mt-[2px] mr-[0.5rem]">
                        <img
                          width="20"
                          height="20"
                          :src="getImageUrl('assets/icons/quote_checkbox_received.svg')"
                          alt="checkbox"
                        />
                      </div>
                      <div class="checkbox-text flex items-center gap-2">
                        <p class="text-base whitespace-nowrap font-semibold text-main">
                          Jetex FBO, Paris
                        </p>
                        <p class="text-sm whitespace-nowrap text-subtitle">(Quote Received)</p>
                      </div>
                    </div>
                  </div>
                </div>
              </ScrollBar>
            </template>
          </OrderForm>
        </div>
        <div class="order-modal-footer">
          <button class="modal-button cancel" @click.stop="emit('modal-close')">Cancel</button>
          <button class="modal-button submit" @click.stop="onValidate()">Send</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { computed, ref } from 'vue';
import { onClickOutside } from '@vueuse/core';
import OrderForm from '@/components/forms/OrderForm.vue';
import { getImageUrl } from '@/helpers';
import { notify } from '@/helpers/toast';
import CheckboxField from '../forms/fields/CheckboxField.vue';
import InputField from '../forms/fields/InputField.vue';
import ScrollBar from '../forms/ScrollBar.vue';

defineProps({
  isOpen: Boolean
});

const emit = defineEmits(['modal-close', 'modal-submit']);
const target = ref(null);

const note = ref('');
const isPinned = ref(false);
const email = ref('');

onClickOutside(target, () => emit('modal-close'));

const isValidEmail = computed(() => /^[^@]+@[^@]+\.[^@]+$/.test(email.value));

const onValidate = async () => {
  const isValid = note.value;
  if (!isValid) {
    return notify('Error while submitting, form is not valid!', 'error');
  } else {
    emit('modal-submit');
    emit('modal-close');
  }
};
</script>

<style scoped lang="scss">
.quote-modal {
  &-text {
    &-content {
      font-size: 15px;
    }

    &-description {
      font-size: 12px;
    }
  }

  .hover-wrap {
    &:hover {
      .quote-modal-tooltip {
        display: block;
      }
    }
    .filter-red {
      filter: brightness(0) saturate(100%) invert(46%) sepia(68%) saturate(1603%) hue-rotate(326deg)
        brightness(108%) contrast(100%);
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
    bottom: 1.8rem;
    left: 0;
    min-width: 27vw;

    li {
      font-size: 12px;
      font-weight: 400;
    }

    &::before {
      content: '';
      position: absolute;
      width: 10px;
      height: 10px;
      background-color: rgb(81, 93, 138);
      transform: rotate(45deg);
      left: 6.7rem;
      bottom: -5px;
    }
  }
}
</style>
