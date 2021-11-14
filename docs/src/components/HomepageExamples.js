import React from "react";
import Tabs from "@theme/Tabs";
import TabItem from "@theme/TabItem";
import CodeBlock from "@theme/CodeBlock";

const Examples = [
  {
    label: "Client",
    value: "default",
    path: "client.py",
    isDefault: true,
    content: `from netlib import Client,

c = Client("127.0.0.1", 7092)

@c.OnSignal("/greetings")
def handle_greeting(signal):
    print("Hello, World!")`,
  },
];

function Example({ label, value, path, content, isDefault }) {
  return (
    <>
      {isDefault ? (
        <TabItem value={value} label={label} default>
          <CodeBlock metastring={`title="${path}"`}>{content}</CodeBlock>
        </TabItem>
      ) : (
        <TabItem value={value} label={label}>
          <CodeBlock metastring={`title="${path}"`}>{content}</CodeBlock>
        </TabItem>
      )}
    </>
  );
}

export default function HomepageExamples() {
  return (
    // <Tabs>
    //   <TabItem value="apple" label="Apple" default></TabItem>
    //   <TabItem value="app" label="Apple"></TabItem>
    // </Tabs>

    <Tabs>
      {Examples.map((props, i) => {
        return <Example idx={i} {...props} />;
      })}
    </Tabs>
  );
}
