<script setup>
import { reactive, computed, ref } from "vue";
import { ElMessage } from "element-plus";
import axios from "../axios";
import sha256 from "crypto-js/sha256";

const props = defineProps(["modelValue"]);
const emit = defineEmits(["update:modelValue"]);
const form = ref(null);
const visible = computed({
    get() {
        return props.modelValue;
    },
    set(value) {
        emit("update:modelValue", value);
    },
});

const passwdSet = reactive({
    old: "",
    new: "",
    repeat: "",
});

const validatePasswd = (rule, val, callback) => {
    if (val == passwdSet.old) {
        callback(new Error("The old and the new are the same."));
    } else if (/^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$/.test(val)) {
        callback();
    } else {
        callback(
            new Error(
                "Password should include both alphabets and digits, and be longer than 8 characters."
            )
        );
    }
};

const validateRepeat = (rule, val, callback) => {
    if (val == passwdSet.new) {
        callback();
    } else {
        callback(new Error("Password repeated is not the same as the above."));
    }
};

const rules = {
    new: [{ validator: validatePasswd, trigger: "blur" }],
    repeat: [{ validator: validateRepeat, trigger: "blur" }],
};

const submitRequest = () => {
    form.value.validate((result) => {
        if (result) {
            axios
                .post("/passwd", {
                    old: sha256(passwdSet.old).toString(),
                    new: sha256(passwdSet.new).toString(),
                })
                .then((response) => {
                    if (response.data.result == "success") {
                        visible.value = false;
                        ElMessage.success("Password setting succeeded.");
                    }
                });
        }
    });
};
</script>

<template>
    <el-dialog
        v-model="visible"
        title="Set Password"
        class="w-4/5 md:3/5 lg:w-2/5"
    >
        <el-form
            :rules="rules"
            :model="passwdSet"
            ref="form"
            label-width="33%"
            :inline-message="true"
        >
            <div class="m-8">
                <el-form-item label="Origin Password" prop="old">
                    <el-input
                        placeholder="Origin Password"
                        v-model="passwdSet.old"
                        type="password"
                        autocomplete="current-password"
                    >
                    </el-input>
                </el-form-item>
                <el-form-item label="New Password" prop="new">
                    <el-input
                        placeholder="New Password"
                        v-model="passwdSet.new"
                        type="password"
                        autocomplete="new-password"
                    >
                    </el-input>
                </el-form-item>
                <el-form-item label="Repeat Password" prop="repeat">
                    <el-input
                        placeholder="Repeat Password"
                        v-model="passwdSet.repeat"
                        type="password"
                        @enter="submitRequest"
                        autocomplete="new-password"
                    >
                    </el-input>
                </el-form-item>
            </div>
        </el-form>
        <template #footer>
            <span class="dialog-footer">
                <el-button @click="visible = false">Cancel</el-button>
                <el-button type="primary" @click="submitRequest">
                    Confirm
                </el-button>
            </span>
        </template>
    </el-dialog>
</template>
