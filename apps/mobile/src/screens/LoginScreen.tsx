import React, { useState } from "react";
import { Button, Text, TextInput, View } from "react-native";
import { CurrentUser, getMe, login } from "../api/client";
import { t } from "../i18n";

interface Props {
  onAuthenticated: (user: CurrentUser) => void;
}

/** Email/password login screen (VIS-2). Tokens are persisted via the secure
 * token storage abstraction in api/secureStore. */
export function LoginScreen({ onAuthenticated }: Props): React.JSX.Element {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  async function onSubmit(): Promise<void> {
    setError(null);
    setSubmitting(true);
    try {
      await login(email, password);
      onAuthenticated(await getMe());
    } catch {
      setError(t("auth.invalidCredentials"));
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <View style={{ padding: 24, gap: 12 }}>
      <Text style={{ fontSize: 20, fontWeight: "600" }}>{t("auth.signIn")}</Text>
      <TextInput
        placeholder={t("auth.email")}
        autoCapitalize="none"
        keyboardType="email-address"
        value={email}
        onChangeText={setEmail}
        style={{ borderWidth: 1, borderColor: "#ccc", padding: 8 }}
      />
      <TextInput
        placeholder={t("auth.password")}
        secureTextEntry
        value={password}
        onChangeText={setPassword}
        style={{ borderWidth: 1, borderColor: "#ccc", padding: 8 }}
      />
      {error ? <Text style={{ color: "crimson" }}>{error}</Text> : null}
      <Button
        title={submitting ? t("auth.signingIn") : t("auth.signIn")}
        onPress={onSubmit}
        disabled={submitting}
      />
    </View>
  );
}
