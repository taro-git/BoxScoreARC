<template>
  <v-container>
    <v-data-table
      :headers="headers"
      :items="licenses"
      item-key="name"
      class="elevation-1 bg-darken"
      :items-per-page="10"
    >
      <!-- Repository -->
      <template v-slot:[`item.repository`]="{ item }">
        <a v-if="item.repository" :href="item.repository" target="_blank">
          {{ item.repository }}
        </a>
      </template>

      <!-- License Text -->
      <template v-slot:[`item.licenseText`]="{ item }">
        <v-expansion-panels>
          <v-expansion-panel class="bg-lighten">
            <v-expansion-panel-title>View</v-expansion-panel-title>
            <v-expansion-panel-text>
              <pre class="text-body-2 whitespace-pre-wrap">
                                {{ item.licenseText || "N/A" }}
                            </pre
              >
            </v-expansion-panel-text>
          </v-expansion-panel>
        </v-expansion-panels>
      </template>

      <!-- Notice -->
      <template v-slot:[`item.noticeFile`]="{ item }">
        <v-expansion-panels>
          <v-expansion-panel class="bg-lighten">
            <v-expansion-panel-title>View</v-expansion-panel-title>
            <v-expansion-panel-text>
              <pre class="text-body-2 whitespace-pre-wrap">
                                {{ item.noticeFile || "N/A" }}
                            </pre
              >
            </v-expansion-panel-text>
          </v-expansion-panel>
        </v-expansion-panels>
      </template>
    </v-data-table>
  </v-container>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";

interface LicenseInfo {
  name: string;
  version: string;
  licenses: string;
  repository?: string;
  publisher?: string;
  licenseText?: string;
  noticeFile?: string;
}

const headers = [
  { title: "Package", key: "name" },
  { title: "Version", key: "version" },
  { title: "License", key: "licenses" },
  { title: "Publisher", key: "publisher" },
  { title: "Repository", key: "repository" },
  { title: "License Text", key: "licenseText" },
  { title: "Notice", key: "noticeFile" },
];

const licenses = ref<LicenseInfo[]>([]);

//
// load init data
// -------------------------------------------------------------------
onMounted(async () => {
  const res = await fetch("/view/assets/licenses.json");
  const data: LicenseInfo = await res.json();

  licenses.value = Object.entries(data).map(
    ([, info]: [string, LicenseInfo]) => {
      return {
        name: info.name,
        version: info.version,
        licenses: info.licenses,
        repository: info.repository,
        publisher: info.publisher,
        licenseText: info.licenseText,
        noticeFile: info.noticeFile,
      };
    },
  );
});
</script>
