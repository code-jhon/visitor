import React, { useEffect, useState } from "react";
import { SafeAreaView, Text, View } from "react-native";
import { getHealth } from "./api/client";
import { t } from "./i18n";

export default function App(): React.JSX.Element {
  const [status, setStatus] = useState<string>("...");

  useEffect(() => {
    getHealth()
      .then((h) => setStatus(h.status))
      .catch(() => setStatus("unreachable"));
  }, []);

  return (
    <SafeAreaView>
      <View style={{ padding: 24 }}>
        <Text style={{ fontSize: 24, fontWeight: "600" }}>{t("app.title")}</Text>
        <Text>
          {t("app.apiStatus")}: {status}
        </Text>
      </View>
    </SafeAreaView>
  );
}
