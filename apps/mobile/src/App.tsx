import React, { useEffect, useState } from "react";
import { Button, SafeAreaView, Text, View } from "react-native";
import { CurrentUser, getHealth, logout } from "./api/client";
import { LoginScreen } from "./screens/LoginScreen";
import { t } from "./i18n";

export default function App(): React.JSX.Element {
  const [status, setStatus] = useState<string>("...");
  const [user, setUser] = useState<CurrentUser | null>(null);

  useEffect(() => {
    getHealth()
      .then((h) => setStatus(h.status))
      .catch(() => setStatus("unreachable"));
  }, []);

  async function onSignOut(): Promise<void> {
    await logout();
    setUser(null);
  }

  return (
    <SafeAreaView>
      <View style={{ padding: 24, gap: 8 }}>
        <Text style={{ fontSize: 24, fontWeight: "600" }}>{t("app.title")}</Text>
        <Text>
          {t("app.apiStatus")}: {status}
        </Text>
        {user ? (
          <View style={{ gap: 8 }}>
            <Text>
              {t("auth.signedInAs")}: {user.email} (
              {user.roles.map((r) => r.name).join(", ")})
            </Text>
            <Button title={t("auth.signOut")} onPress={onSignOut} />
          </View>
        ) : (
          <LoginScreen onAuthenticated={setUser} />
        )}
      </View>
    </SafeAreaView>
  );
}
