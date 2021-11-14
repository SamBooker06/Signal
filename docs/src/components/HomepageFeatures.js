import React from "react";
import clsx from "clsx";
import styles from "./HomepageFeatures.module.css";

const FeatureList = [
  {
    title: "Event-Driven",
    description: (
      <>Signal is event-driven; no messy file systems or hard-coded handlers.</>
    ),
  },
  {
    title: "Simple",
    description: (
      <>
        Signal&apos;s simple syntax and allows for it to be easily read and
        written.
      </>
    ),
  },
  {
    title: "Expandable",
    description: (
      <>
        Signal is designed to be easily expanded and scale for larger
        applications.
      </>
    ),
  },
];

function Feature({ Svg, title, description }) {
  return (
    <div className={clsx("col col--4")}>
      <div className="text--center">
        {Svg ? <Svg className={styles.featureSvg} alt={title} /> : null}
      </div>
      <div className="text--center padding-horiz--md">
        <h3>{title}</h3>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
