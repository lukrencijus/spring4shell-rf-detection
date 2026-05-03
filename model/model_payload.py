import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.utils import shuffle
from sklearn.metrics import classification_report
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

df = pd.read_csv('../dataset.csv')

df['packet_ratio'] = df['src2dst_packets'] / (df['dst2src_packets'] + 1)
df['ack_ratio'] = df['bidirectional_ack_packets'] / (df['bidirectional_packets'] + 1)
df['duration_ratio'] = df['src2dst_duration_ms'] / (df['bidirectional_duration_ms'] + 1)

required_fields = [
    'label', 'bidirectional_packets',
    'src2dst_packets',  'dst2src_packets', 'bidirectional_syn_packets',
    'bidirectional_ack_packets', 'bidirectional_psh_packets', 'src2dst_syn_packets', 'src2dst_ack_packets', 'src2dst_psh_packets',
    'dst2src_syn_packets', 'dst2src_ack_packets', 'dst2src_psh_packets', 'packet_ratio', 'ack_ratio', 'duration_ratio',
    'raw_payload'
]

# Split dataframes according to their purpose
df_learning = df[df['split'] == 'learning']
df_validating = df[df['split'] == 'validating']
df_testing = df[df['split'] == 'testing']

df_learning = shuffle(df_learning[required_fields])
df_validating = df_validating[required_fields]
df_testing = shuffle(df_testing[required_fields])

X_train = df_learning.iloc[:, 1:len(required_fields)]
y_train = df_learning.iloc[:, 0]

X_test = df_testing.iloc[:, 1:len(required_fields)]
y_test = df_testing.iloc[:, 0]

# This preprocessor handles specific keywords or symbols
preprocessor = ColumnTransformer(
    transformers=[
        ('num', 'passthrough', X_train.columns[:-1].tolist()),
        ('char_count', TfidfVectorizer(
            analyzer='char',
            ngram_range=(1, 1),
            vocabulary=['=']
        ), 'raw_payload'),
        ('keyword_count', TfidfVectorizer(
            vocabulary=['cmd', 'shell', 'jsp', 'class', 'runtime']
        ), 'raw_payload')
    ]
)

# Random forest without parameters
rf = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier())
])
rf.fit(X_train, y_train)

y_pred = rf.predict(X_test)
print(rf.score(X_test, y_test))

# Mapping feature names for the importance list
char_names = [f"char_{c}" for c in ['=']]
key_names = [f"key_{k}" for k in ['cmd', 'shell', 'jsp', 'class', 'runtime']]
all_feature_names = X_train.columns[:-1].tolist() + char_names + key_names

features = pd.Series(
    rf.named_steps['classifier'].feature_importances_,
    index=all_feature_names
).sort_values(ascending=False)
print(features)

print(classification_report(y_test, y_pred))

# Random forest with parameters
# 100 trees, randomizes data when building trees, balanced weight (difference between malicious packet and not count)
rf2 = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(
        n_estimators=300,
        random_state=42,
        max_depth=None,
        min_samples_split=10,
        min_samples_leaf=5,
        max_features='sqrt',
        class_weight='balanced_subsample',
        n_jobs=-1
    ))
])
rf2.fit(X_train, y_train)

y_pred = rf2.predict(X_test)
print(rf2.score(X_test, y_test))

features = pd.Series(
    rf2.named_steps['classifier'].feature_importances_,
    index=all_feature_names
).sort_values(ascending=False)
print(features)

print(classification_report(y_test, y_pred))
