import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.utils import shuffle
from sklearn.metrics import classification_report

df = pd.read_csv('../dataset.csv')

# Duration is maybe unnecessary as the delays that were simulated don't differentiate that much
required_fields = [ 'label', 'bidirectional_packets', 
                    'src2dst_packets',  'dst2src_packets', 'bidirectional_syn_packets',
                    'bidirectional_ack_packets', 'bidirectional_psh_packets', 'src2dst_syn_packets', 'src2dst_ack_packets', 'src2dst_psh_packets',
                    'dst2src_syn_packets', 'dst2src_ack_packets', 'dst2src_psh_packets', 
                    'dst2src_duration_ms', 'src2dst_duration_ms', 'bidirectional_duration_ms' ]
# 'dst2src_min_ps' 'src2dst_min_ps' 'src2dst_mean_ps' 'src2dst_max_ps', 'dst2src_max_ps', 'dst2src_mean_ps', 'src2dst_bytes', 'dst2src_bytes', 'bidirectional_bytes',
# Removed due to size fingerprinting caused by insufficient size in benign traffic packets
# Results in > 0.99 accuracy
# To avoid this simulation of larger http pcakets could be used.
# I think the ability to compare payload matters in this project due to spring4shell commands starting with cmd= as well as the initial payload being identical

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

# Random forest without parameters
# Accuracy of 0.84, but heavily relies on duration between packets (not a reliable feature, because it can shift due to internet connections)
rf = RandomForestClassifier()
rf.fit(X_train, y_train)

y_pred = rf.predict(X_test)
print(rf.score(X_test, y_test))

features = pd.Series(
    rf.feature_importances_,
    index=X_train.columns
).sort_values(ascending=False)
print(features)

print(classification_report(y_test, y_pred))

# Random forest with parameters
# 100 trees, randomizes data when building trees, balanced weight (difference between malicious packet and not count)
# Result is 0.838, still heavily relies on packet duration
rf2 = RandomForestClassifier(
    n_estimators = 100,
    random_state = 42,
    class_weight = 'balanced',
    n_jobs=-1
)
rf2.fit(X_train, y_train)

y_pred = rf2.predict(X_test)
print(rf2.score(X_test, y_test))

features = pd.Series(
    rf2.feature_importances_,
    index=X_train.columns
).sort_values(ascending=False)
print(features)

print(classification_report(y_test, y_pred))

